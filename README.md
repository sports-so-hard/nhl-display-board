# NHL Display Board

A Streamlit app to explore NHL seasons, teams, and rosters. This is an initial scaffold with a clean package structure; data access is currently stubbed and will be backed by `nhl-api-py` in future iterations.

## Environment Setup

Follow the steps below to prepare your development environment with Miniconda and Git (SSH), clone the repo, and then create the project’s conda environment from `environment.yml`.

### 1) Install Miniconda <small>_(if needed)_</small>
Choose your operating system and follow the official [**Miniconda** instructions](https://docs.anaconda.com/miniconda/). The platform-specific installers are available [here](https://www.anaconda.com/download/success).

Notes:
- Use *Miniconda* (the minimal installer), _not_ the full Anaconda Distribution.
- After installation, open a new terminal/session so `conda` is on your PATH.

### 2) Git and GitHub (SSH) prerequisites <small>_(if needed)_</small>
- If you don't have one, create a GitHub account: https://github.com/signup
- Install command-line Git if not already installed (select your OS): https://git-scm.com/downloads
- If you haven't already, generate an SSH key and add it to your SSH agent:
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
- If necessary, add your public key to your GitHub account:
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
- Test your SSH connection:
  ```bash
  ssh -T git@github.com
  ```
  You should see a success message from GitHub if everything is set up correctly.

### 3) Clone the repository <small>_(one time setup)_</small>

```
git clone git@github.com:sports-so-hard/nhl-display-board.git
cd nhl-display-board
```

### 4) Create the Conda Environment <small>_(one time setup)_</small>

Open your terminal (Anaconda Prompt on Windows, Terminal on macOS/Linux) in the project directory and run the following command. This will create a new environment named `nhl-display-board` with all the necessary packages.

```
conda env create -f local-dev/environment.yml
```

Conda will solve the dependencies and download all the required packages. This might take a few minutes.

### 5) Activate the Environment (to use the environment)

Once the creation is complete, activate your new environment:

```
conda activate nhl-display-board
```

Your terminal prompt should now be prefixed with `(nhl-display-board)` and executables from the environment will be used instead of system ones.

#### Deactivate the Environment

To deactivate the environment, and return to default system executables, run
```
conda deactivate
```

## Run the app

1. Activate the environment (if necessary, see above).

2. Run the app.

   ```bash
   streamlit run app/web/display_board_app.py
   ```
