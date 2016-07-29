#  encdec.py - A gedit plugin to encode and decode text to various formats 
#  
# Copyright (c) 2010, Jacques Louw
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY <copyright holder> ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import gedit
import gtk
import base64
import urllib
import binascii
import htmlentitydefs
import re
import hashlib

from gettext import gettext as _

ui_str = """<ui>
	<menubar name="MenuBar">
		<menu name="EditMenu" action="Edit">
			<placeholder name="EditOps_4">
				<separator />
				<menu name="EDP_Menu_Encode" action="EDP_Menu_Encode">
					<menuitem name="EDP_EncB64" action="EDP_EncB64" />
					<menuitem name="EDP_EncURL" action="EDP_EncURL" />
					<menuitem name="EDP_EncHTML" action="EDP_EncHTML" />
					<menuitem name="EDP_EncASCIIHex" action="EDP_EncASCIIHex" />
				</menu>
				<menu name="EDP_Menu_Decode" action="EDP_Menu_Decode">
					<menuitem name="EDP_DecB64" action="EDP_DecB64" />
					<menuitem name="EDP_DecURL" action="EDP_DecURL" />
					<menuitem name="EDP_DecHTML" action="EDP_DecHTML" />
					<menuitem name="EDP_DecASCIIHex" action="EDP_DecASCIIHex" />
				</menu>
				<menu name="EDP_Menu_Hash" action="EDP_Menu_Hash">
					<menuitem name="EDP_HashMD4" action="EDP_HashMD4" />
					<menuitem name="EDP_HashMD5" action="EDP_HashMD5" />
					<menuitem name="EDP_HashSHA1" action="EDP_HashSHA1" />
					<menuitem name="EDP_HashSHA224" action="EDP_HashSHA224" />
					<menuitem name="EDP_HashSHA256" action="EDP_HashSHA256" />
					<menuitem name="EDP_HashSHA384" action="EDP_HashSHA384" />
					<menuitem name="EDP_HashSHA512" action="EDP_HashSHA512" />
				</menu>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""

def decode_htmlentities(string):
    def substitute_entity(match):
        ent = match.group(3)
        if match.group(1) == "#":
            if match.group(2) == '':
                return unichr(int(ent))
            elif match.group(2) == 'x':
                return unichr(int('0x'+ent, 16))
        else:
            cp = htmlentitydefs.name2codepoint.get(ent)
            if cp: return unichr(cp)
            else: return match.group()
    entity_re = re.compile(r'&(#?)(x?)(\w+);')
    return entity_re.subn(substitute_entity, string)[0]
    
def encode_htmlentities(string):
	t = ""
	for i in string:
		if ord(i) in htmlentitydefs.codepoint2name:
			name = htmlentitydefs.codepoint2name.get(ord(i))
			t += "&" + name + ";"
		else:
			t += i
	return t

class EncDecWindowHelper:

	def __init__(self, plugin, window):
		# Set up menu
		self.action_group = gtk.ActionGroup("EncDecPluginActions")
		self.action_group.add_actions([
			("EDP_Menu_Encode", None, _("Encode"), None, None,	None),
			("EDP_Menu_Decode", None, _("Decode"), None, None, None),
			("EDP_Menu_Hash", None, _("Hash"), None, None, None),
			("EDP_EncB64", None, _("Base64"), None, _("Encode to Base64 encoding"), lambda a: self.encdecode("b64","enc")),
			("EDP_DecB64", None, _("Base64"), None, _("Decode to Base64 encoding"), lambda a: self.encdecode("b64","dec")),
			("EDP_EncURL", None, _("URL"), None, _("Encode to URL encoding"), lambda a: self.encdecode("url","enc")),
			("EDP_DecURL", None, _("URL"), None, _("Decode to URL encoding"), lambda a: self.encdecode("url","dec")),
			("EDP_EncHTML", None, _("HTML"), None, _("Encode to HTML encoding"),lambda a: self.encdecode("html","enc")),
			("EDP_DecHTML", None, _("HTML"), None, _("Decode to HTML encoding"),lambda a: self.encdecode("html","dec")),
			("EDP_EncASCIIHex", None, _("ASCII Hex"),None,_("Encode to ASCII Hex"),	lambda a: self.encdecode("asciihex","enc")),
			("EDP_DecASCIIHex", None, _("ASCII Hex"),None,_("Decode to ASCII Hex"),	lambda a: self.encdecode("asciihex","dec")),
			("EDP_HashMD4", None, _("MD4"),None,_("MD4 Hash of the string"),	lambda a: self.hash_string("md4")),
			("EDP_HashMD5", None, _("MD5"),None,_("MD5 Hash of the string"),	lambda a: self.hash_string("md5")),
			("EDP_HashSHA1", None, _("SHA1"),None,_("SHA1 Hash of the string"),	lambda a: self.hash_string("sha1")),
			("EDP_HashSHA224", None, _("SHA224"),None,_("SHA224 Hash of the string"),	lambda a: self.hash_string("sha224")),
			("EDP_HashSHA256", None, _("SHA256"),None,_("SHA256 Hash of the string"),	lambda a: self.hash_string("sha256")),
			("EDP_HashSHA384", None, _("SHA384"),None,_("SHA384 Hash of the string"),	lambda a: self.hash_string("sha384")),
			("EDP_HashSHA512", None, _("SHA512"),None,_("SHA512 Hash of the string"),	lambda a: self.hash_string("sha512"))
		])

		manager = window.get_ui_manager()
		manager.insert_action_group(self.action_group, -1)
		ui_id = manager.add_ui_from_string(ui_str)
		window.set_data("EncDecPluginUIId", ui_id)
		self._window = window
		self.update_ui()

	def deactivate(self):
		window = self._window
		ui_id = window.get_data("EncDecPluginUIId")
		manager = window.get_ui_manager()
		manager.remove_ui(ui_id)
		manager.remove_action_group(self.action_group)
		manager.ensure_update()

	def update_ui(self):
		pass
		
	def encdecode(self, encoding, direction):
		view = self._window.get_active_view()
		doc = self._window.get_active_document()
		view.cut_clipboard();
		string = gtk.clipboard_get().wait_for_text()
		try:
			if (direction == "enc"):
				encode = True
			else:
				encode = False
		
			if encoding == "b64":
				if encode:
					result = binascii.b2a_base64(string)
				else:
					result = binascii.a2b_base64(string)
			elif encoding == "url":
				if encode:
					result = urllib.quote_plus(string)
				else:
					result = urllib.unquote_plus(string)
			elif encoding == "html":
				if encode:
					result = encode_htmlentities(string)
				else:
					result = decode_htmlentities(string)
			elif encoding == "asciihex":
				if encode:
					result = binascii.hexlify(string)
				else:
					result = binascii.unhexlify(string)
		except Exception as e:
			result = "[encdecplugin - error: "+str(e)+"]"
		else:
			try:
				unicode(result, "utf-8")
			except Exception as e:
				result = "[encdecplugin - binary result: "+re.sub('([0-9a-f]{2})',r'\1 ',binascii.hexlify(result))+"]"
		
		doc.insert_at_cursor(result)
		return True
		
	def hash_string(self, method):
		view = self._window.get_active_view()
		doc = self._window.get_active_document()
		view.cut_clipboard();
		string = gtk.clipboard_get().wait_for_text()
		
		if method == "md4":
			h = hashlib.new('md4')
			h.update(string)
			result = h.hexdigest()
		elif method == "md5":
			result = hashlib.md5(string).hexdigest()
		elif method == "sha1":
			result = hashlib.sha1(string).hexdigest()
		elif method == "sha224":
			result = hashlib.sha224(string).hexdigest()
		elif method == "sha256":
			result = hashlib.sha256(string).hexdigest()
		elif method == "sha384":
			result = hashlib.sha384(string).hexdigest()
		elif method == "sha512":
			result = hashlib.sha512(string).hexdigest()
		
		doc.insert_at_cursor(result)
		return True

class EncDecPlugin(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
		self._instances = {}

	def activate(self, window):
		self._instances[window] = EncDecWindowHelper(self, window)

	def deactivate(self, window):
		self._instances[window].deactivate()
		del self._instances[window]

	def update_ui(self, window):
		self._instances[window].update_ui()

