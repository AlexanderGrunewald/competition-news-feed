# competition-news-feed
A newsfeed tool that enables the monitoring of new product launches of competitors


# Windows Setup Guide: Pixi & DuckDB CLI

This guide covers setting up **Pixi** (package and environment manager) and the **DuckDB CLI** on Windows (x86_64).

---

## 1. Install Pixi

Open PowerShell (Run as Administrator or as a standard user) and execute:

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

### Verification
Restart your PowerShell terminal and verify the installation:

```powershell
pixi --version
```

> **Note:** If `pixi` is not recognized, ensure your user profile's `.pixi/bin` path is added to your environment `PATH` variable:
> ```powershell
> [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\.pixi\bin", [EnvironmentVariableTarget]::User)
> ```

---

## 2. Install DuckDB CLI

Because `duckdb-cli` is not distributed via `conda-forge` for `win-64`, install it directly on your system using **winget** or manual installation.

### Option A: Via Windows Package Manager (`winget`) — Recommended

Run the following command in PowerShell:

```powershell
winget install DuckDB.cli
```

#### Persisting PATH for Winget Installations
Winget installs portable CLI tools into the user AppData directory. To ensure `duckdb` is accessible across any terminal session:

1. Restart PowerShell and test:
   ```powershell
   duckdb --version
   ```
2. If PowerShell returns a `CommandNotFoundException`, manually register the installation directory to your User `PATH`:
   ```powershell
   $targetDir = (Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "duckdb.exe" -Recurse).DirectoryName
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$targetDir", [EnvironmentVariableTarget]::User)
   $env:Path += ";$targetDir"
   ```

---

### Option B: Manual Installation

1. Download the latest Windows binary release from the [DuckDB GitHub Releases](https://github.com/duckdb/duckdb/releases) (`duckdb_cli-windows-amd64.zip`).
2. Extract `duckdb.exe` to a permanent location (e.g., `C:\Tools\duckdb\`).
3. Add that directory to your User `PATH`:
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\duckdb", [EnvironmentVariableTarget]::User)
   ```

---

## 3. Configuring Projects with `pixi.toml` on Windows

When configuring a cross-platform Pixi project (macOS/Linux/Windows):

1. **Keep `duckdb-cli` out of the root `[dependencies]`:** Conda-forge does not have a `win-64` package for the standalone CLI. Place `duckdb-cli` under `[target.linux-64.dependencies]` and `[target.osx-arm64.dependencies]`.
2. **Use the DuckDB Python library inside the environment:** Add the Python API bindings under general dependencies:
   ```toml
   [dependencies]
   duckdb = ">=1.5.5,<2"
   ```
3. **Handle SQL script redirects safely:** Windows Command Prompt and PowerShell do not reliably handle `< schema.sql` input redirection in Pixi tasks. Use DuckDB's internal `.read` command instead:

```toml
[target.win-64.tasks]
init-db = 'duckdb data/database/newsFeed.duckdb ".read src/db/schema.sql"'
```

---

## 4. Quick Verification Checklist

Open a fresh PowerShell prompt in your repository and run:

```powershell
# 1. Check tool accessibility
pixi --version
duckdb --version

# 2. Install workspace dependencies
pixi install

# 3. Test running tasks via Pixi
pixi run init-db
```
