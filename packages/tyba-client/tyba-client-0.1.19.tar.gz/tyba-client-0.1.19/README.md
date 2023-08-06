# Tyba API Client

### Run the examples in this codebase
- Establish a SSH connection to the AWS bastion (enables access to the pricing DB)
- Start the Generation docker image
- Start the Tyba Server REPL
- Finally, run the example script shown below in a virtual environment (provided by poetry):
```
poetry shell
poetry install
HOST='http://localhost:3000' TYBA_PAT="dev-test-api-key"   python3 examples/pv_example.py
```

### Common Error Scenarios:
#### Receiving a 401 Response
- Check that the request is hitting the Tyba Server REPL
- Check that the request is making it to the intended domain. (e.g., make sure the implementation of `Client` is reading the `HOST` env var)