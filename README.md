# GPandas Documentation

This repository contains the source code for the official [GPandas documentation website](<adding the url here later>). The site is built using [Hugo](https://gohugo.io/) and the [LotusDocs theme](https://github.com/colinwilson/lotusdocs).

GPandas is a high-performance data manipulation library for Go, inspired by Python's pandas. The initial idea was to make it easy for python folks to transition to golang with as less of friction as possible.

## Prerequisites

Before running the documentation site locally, you need to have the following installed:

1. **Hugo (Extended version recommended)** - [Installation guide](https://gohugo.io/installation/)
   - macOS: `brew install hugo`
   - Windows: `choco install hugo-extended` or `scoop install hugo-extended`
   - Linux: Check the [installation page](https://gohugo.io/installation/linux/) for your distribution
   
2. **Go (version 1.18 or later)** - Required for Hugo Modules
   - Download from [https://golang.org/dl/](https://golang.org/dl/)

3. **Git** - For cloning the repository and Hugo Modules

## Running the Documentation Site Locally

1. **Clone the repository:**
```bash
git clone https://github.com/apoplexi24/gpandas_docs.git
cd gpandas_docs
```

2. **Initialize Hugo modules (first time only):**
```bash
hugo mod init github.com/apoplexi24/gpandas_docs
```

3. **Get module dependencies:**
```bash
hugo mod get
```

4. **Start the Hugo server:**
```bash
hugo server
```

The site will be available at `http://localhost:1313/`.

## Contributing

Contributions to the documentation are welcome! Please feel free to open an issue or submit a pull request if you find any errors or have suggestions for improvement.

To contribute:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make your edits in the `content` directory.
4. Test your changes locally by running `hugo server`.
5. Submit a pull request.

## License

The documentation is licensed under the [MIT License](LICENSE).

## Note from Apoplexi

I believe in keeping the docs open source like the gpandas package, hence here's the docs repo made public. Most of the docs is AI generated and is manually vetted by me for misinformation and hallucinations.
