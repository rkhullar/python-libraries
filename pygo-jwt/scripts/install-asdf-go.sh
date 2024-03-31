#!/usr/bin/env sh
if command -v go; then exit; fi
git clone https://github.com/asdf-vm/asdf.git "$ASDF_DIR" --branch "v${ASDF_VERSION}"
. "$ASDF_DIR/asdf.sh"
asdf plugin-add golang
asdf install golang "$GO_VERSION"
ln -s "$HOME/.asdf/installs/golang/${GO_VERSION}/go/bin/go" /usr/local/bin/go
