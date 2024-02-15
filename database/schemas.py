user_schemas = [
  """ CREATE TABLE IF NOT EXISTS security (
        id VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    );
  """,
  """ CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(255) PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        house_num VARCHAR(255),
        street VARCHAR(255),
        postcode VARCHAR(255),
        phone_num VARCHAR(255),
        CONSTRAINT fk_users_security FOREIGN KEY (id) REFERENCES security(id)
    );
  """,
  """ CREATE TABLE IF NOT EXISTS resets (
        id VARCHAR(255) PRIMARY KEY,
        token BOOLEAN NOT NULL,
        assigned VARCHAR(255) NOT NULL,
        FOREIGN KEY (assigned) REFERENCES security(id)
    );
  """
]

court_schema = """
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    day DATE NOT NULL,
    seven VARCHAR(255) NOT NULL,
    eight VARCHAR(255) NOT NULL,
    nine VARCHAR(255) NOT NULL,
    ten VARCHAR(255) NOT NULL,
    eleven VARCHAR(255) NOT NULL,
    twelve VARCHAR(255) NOT NULL,
    thirteen VARCHAR(255) NOT NULL,
    fourteen VARCHAR(255) NOT NULL,
    fifteen VARCHAR(255) NOT NULL,
    sixteen VARCHAR(255) NOT NULL,
    seventeen VARCHAR(255) NOT NULL,
    eighteen VARCHAR(255) NOT NULL
);
"""

court_headings = ['grass_one', 'grass_two', 'clay_one']