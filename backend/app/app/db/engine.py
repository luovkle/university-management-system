from sqlmodel import create_engine

connect_args = {"check_same_thread": False}

engine = create_engine("sqlite:///app.db", connect_args=connect_args)
