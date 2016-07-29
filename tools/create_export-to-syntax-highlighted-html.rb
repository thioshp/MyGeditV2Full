#!/usr/bin/env ruby2.0
# [Gedit Tool]
# Name=[create] export to syntax highlighted html
# Shortcut=<Primary><Shift>h
# Applicability=all
# Input=document
# Output=new-document
# Save-files=nothing


# Exports the current file to syntax highlighted html using coderay
#  (depends on ruby, coderay, gem, zenity)
#
# Save:   Nothing
# Input:  Current document
# Output: Nothing
#
# by Jan Lelis (mail@janlelis.de), edited by (you?)

require 'rubygems'
require 'coderay'

supported = {
'application/x-ruby' => 'ruby',
'text/html'          => 'html',
'text/rhtml'         => 'rhtml',
'text/css'           => 'css',
'text/x-markdown'    => 'md',
'application/javascript'    => 'java_script',
'text/x-shellscript' => 'sh',
'application/xml'    => 'xml',
'text/x-csrc'        => 'c',
'text/x-chdr'        => 'cplusplus',
'text/x-c++src'      => 'cplusplus',
'text/x-java'        => 'java',
'text/x-php'         => 'php',
'text/x-python'      => 'python',
'text/x-scheme'      => 'scheme',
'text/x-sql'         => 'sql',
'text/plain'		 		 => 'txt',
 # ...
}

if lang = supported[ENV['GEDIT_CURRENT_DOCUMENT_TYPE']]
	html = CodeRay::Duo[lang, :page].highlight gets(nil)
  path = `zenity --file-selection --save --title="Please select the location where the syntax html file should be stored" --filename="$GEDIT_CURRENT_DOCUMENT_PATH.html"`
  unless path.empty?
    File.open(path, 'w').puts html
  end
else
  `zenity --error --text="Sorry, language not supported!!!! Exporting to HTML failed!!!"`
end
