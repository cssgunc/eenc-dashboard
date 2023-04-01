import toml
import os

output_file = "secrets.toml"

abs_path = os.path.abspath("firestore-key.json")
print(abs_path)

with open(abs_path) as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)