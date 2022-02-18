https://cloud.google.com/artifact-registry/docs/python/quickstart

```bash
pipenv install --dev twine keyrings.google-artifactregistry-auth
```

Create a new repository.

```bash
    export REGION=us-west2
export REPO=warn-transformer
gcloud artifacts repositories create $REPO \
    --repository-format=python \
    --location=$REGION \
    --description="Consolidate, enrich and republish the data gathered by warn-scraper"
```

```bash
gcloud config set artifacts/repository $REPO
```

```bash
gcloud config set artifacts/location $REGION
```

```bash
gcloud artifacts print-settings python
```

```bash
make build-release
```

```bash
pipenv run twine upload --repository-url https://us-west2-python.pkg.dev/big-local-news-267923/warn-transformer/ dist/*
```

```
pipenv install --index-url https://us-west2-python.pkg.dev/big-local-news-267923/warn-transformer/ warn-transformer
```
