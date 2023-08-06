# lsl-cli
Command-line tools for the [Lab Streaming Layer](https://labstreaminglayer.readthedocs.io/info/getting_started.html). 

# Installation
### Method 1: Using pip
```bash
pip install lsl-cli
```

### Method 2: From source
```bash
git clone https://github.com/yop0/lsl-cli.git
cd lsl-cli
pip install .
```

## Enabling autocompletion (bash/zsh users)
The package comes with autocompletion files for Bash and Zsh.
To enable autocompletion, use the following command to automatically source the autocompletion file (for Bash users, replace `~/.zshrc`  with `~/.bashrc`): 
```
lsl complete >> ~/.zshrc
```

# Usage
```
$> lsl list                # List available stream outlets
$> lsl show {outlet}       # Show outlet data (in XML format)
$> lsl echo {outlet}       # Continuously print received data
$> lsl find                # Use options to specify outlet properties (e.g. --name, --channel_count, ...)
```
