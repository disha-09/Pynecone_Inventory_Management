import pynecone as pc

config = pc.Config(
    app_name="Pynecone_Inventory_Management",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
