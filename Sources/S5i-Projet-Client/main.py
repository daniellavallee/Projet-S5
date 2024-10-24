import typer
from src.loops import MainLoop, CalibLoop
from src.enums import Hosts

app = typer.Typer(no_args_is_help=True)

@app.command(name="run", no_args_is_help=True)
def main(
        host: Hosts, 
        verbose: bool = False
    ):
    loop = MainLoop(host,is_verbose=verbose)
    loop.run()

@app.command(name="calib", no_args_is_help=True)
def calib(
        host: Hosts
    ):
    loop = CalibLoop(host)
    print(loop.line_follower_cfg)
    loop.run()

if __name__ == "__main__":
    app()