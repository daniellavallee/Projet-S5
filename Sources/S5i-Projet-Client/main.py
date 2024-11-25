import typer
from src.loops import MainLoop, CalibLoop, TestLoop, ReverseLoop
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

@app.command(name="reverse", no_args_is_help=True)
def reverse(
        host: Hosts, 
        verbose: bool = False
    ):
    loop = ReverseLoop(host,is_verbose=verbose)
    loop.run()

@app.command(name="test", no_args_is_help=True)
def test(host: Hosts,verbose: bool = False):
    loop = TestLoop(host,is_verbose=verbose)
    loop.run()

if __name__ == "__main__":
    app()