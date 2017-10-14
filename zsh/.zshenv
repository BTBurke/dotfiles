if [[ $MONOENV != true ]]
then
  export GOPATH="$HOME/projects/golang"
else
  if [[ -d src || $(pwd) =~ "src$" ]]; then
        if [[ -d src ]]; then 
            export GOPATH=$(pwd)
        else
            export GOPATH=$(dirname $(pwd))
        fi
  else
    echo "Monorepo is set but this doesn't appear to be at the root of the repo.  Refusing to set a new GOPATH."
  fi
fi

export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin:/usr/local/git/bin:/usr/local/go/bin:$GOPATH/bin:/usr/local/lib/node/bin"

export ANDROID_HOME="$HOME/Android/Sdk"
export PATH="$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools"

