# ML-Deploy

For IaC, set up the following environment variables:

```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
```

The terraform script will create a bucket for you.
You may copy the files from `data`-folder to your S3 instance.

## Training the model

#### Locally
```sh
./src/titanic/run.sh
```
You can modify the `src/titanic/run.sh` to fit your local needs.

#### In sagemaker
```python
python src/titanic/estimator.py
```
Note that you have to set your own `SAGEMAKER_ROLE` environment variable
