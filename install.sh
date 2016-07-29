#!/bin/sh
# Kill all runing instances if exists
killall gedit

# Register mime types
sudo cp mime/*.xml /usr/share/mime/packages
# Copy language definitions
sudo cp lang-specs/*.lang /usr/share/gtksourceview-2.0/language-specs/
# Update mime type database
sudo update-mime-database /usr/share/mime
# Copy gedit start script
sudo cp -s bin/g /usr/bin/g

# Copy gedit facilities
if [ ! -d $HOME/.gnome2/gedit ]
  then
    mkdir -p ~/.gnome2/gedit
    fi
    # Copy Snippets
    if [ ! -d $HOME/.gnome2/gedit/snippets ]
      then
        mkdir -p ~/.gnome2/gedit/snippets
        fi
        cp snippets/* ~/.gnome2/gedit/snippets/

        # Copy Plugins
        if [ ! -d $HOME/.gnome2/gedit/plugins ]
          then
            mkdir -p ~/.gnome2/gedit/plugins
            fi
            cp -R plugins/* ~/.gnome2/gedit/plugins

            # Copy Styles
            if [ ! -d $HOME/.gnome2/gedit/styles ]
              then
                mkdir -p ~/.gnome2/gedit/styles
                fi
                cp styles/* ~/.gnome2/gedit/styles

