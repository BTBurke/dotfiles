!#/bin/bash

echo "Installing patched fonts for vim-airline..."
git clone https://github.com/powerline/fonts /tmp/fonts
/tmp/fonts/install.sh
rm -rf /tmp/fonts

echo "Installing color themes and snippets..."
mkdir -p ~/.vim
mkdir -p ~/.vim/bundle
mkdir -p ~/.vim/colors
mkdir -p ~/.vim/UltiSnips
cp colors/* ~/.vim/colors/
cp UltiSnips/* ~/.vim/UltiSnips/

echo "Installing vundle to manage plugins..."
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

echo "Symlinking .vimrc to dotfiles/vim/vimrc..."
rm ~/.vimrc
ln -s $(pwd)/vimrc ~/.vimrc

echo "Installation done.\nRun PluginInstall and GoInstallBinaries to complete setup."
