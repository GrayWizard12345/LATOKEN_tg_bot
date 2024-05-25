import psycopg2


def read_conf(path: str = "../.pyway.conf"):
    """
    Reads configuration file into dict
    :param path: a path to config file
    :return: a dict with config
    """
    with open(path) as f:
        conf_file = dict(line.strip().replace(" ", "").split(":", 1) for line in f)
        res = {"user": conf_file["database_username"],
               "password": conf_file["database_password"],
               "host": conf_file["database_host"],
               "port": conf_file["database_port"],
               "dbname": conf_file["database_name"]
               }
        return res


def read_context() -> list:
    """
    Reads context from database
    Returns the freshest 500 messages exchanged due to token limit on openAI
    :return: list of tuples
    """
    with psycopg2.connect(**read_conf()) as conn:
        with conn.cursor() as cur:
            cur.execute(
            """
            SELECT role_, content, name_ 
            FROM chat_bot_context 
            ORDER BY created_at DESC 
            LIMIT 500;
            """
            )
            return cur.fetchall()[::-1]


def write_one_entry(role: str, content: str, name: str = None):
    """
    Writes one entry to database
    :param name: name of the user
    :param role: role of the user
    :param content: content of the message
    :return: None
    """
    with psycopg2.connect(**read_conf()) as conn:
        sql = """
        INSERT INTO chat_bot_context (role_, content, name_) VALUES (%s, %s, %s);
        """
        with conn.cursor() as cur:
            cur.execute(sql, (role, content, name))
            conn.commit()


def get_secret(key_name: str = "OPENAI_KEY"):
    """
    Avoid putting secrets to commits
    :param key_name: a key name
    :return: key value
    """
    with open("../configs.conf") as f:
        conf_file = dict(line.strip().replace(" ", "").split("=", 1) for line in f)
        return conf_file[key_name]


if __name__ == '__main__':
    print(read_conf())
