import yaml


def save_jwt_keys_to_file(
    filename: str,
    **kwargs: dict[str, bytes],
):
    """
    Сохраняет ключи JWT в файл в формате YAML.

    Args:
        filename (str): Путь к файлу, в который будут сохранены ключи.
            По умолчанию: 'src/auth/configs/jwt_key.yaml'.
        kwargs (dict[str, bytes]): Словарь, содержащий ключи JWT
            и их значения в виде байтов.
    """
    with open(filename, 'w') as file:  # noqa: WPS110
        yaml.dump(kwargs, file, default_flow_style=False)
