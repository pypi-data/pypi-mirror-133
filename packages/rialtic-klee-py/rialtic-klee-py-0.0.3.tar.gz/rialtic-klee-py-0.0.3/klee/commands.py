from klee import plans, test
import click, os, sys

@click.group()
# @click.option('-v', 'v_flag', count=True)
def cli():
    if not os.path.exists('oim-engine.json'):
        print("This utility may only be run from within an engine's root directory.")
        sys.exit(0)

@cli.command('build')
@click.argument('targets', nargs = -1)
@click.option('-p', '--plan-type', default = 'default',
    type = click.Choice([*plans.Options], case_sensitive = False))
@click.option('-c', '--claims-dir', default = 'test_claims', help='suggested location: test_cases/json_cases')
@click.option('-o', '--output-dir', default = 'test_cases/json_cases', help="suggested location: test_cases/json_cases")
@click.option('-h', '--history-dir', default = 'test_cases/history', help="suggested location: test_cases/history")
def BuildCommand(targets, plan_type, claims_dir, output_dir, history_dir):
    click.echo(f'Building {",".join(targets) or "all"} targets')

    build_sys = plans.Options[plan_type.lower()] \
        (claims_dir, output_dir, history_dir)
    build_sys.build_node_labels(targets)

@cli.command('test')
@click.argument('targets', nargs = -1)
@click.option('-p', '--plan_type', default = 'default',
    type = click.Choice([*plans.Options], case_sensitive = False))
@click.option('-c', '--claims_dir', default = 'test_claims')
def ExecLocalTest(targets, plan_type, claims_dir):
    if not test.PyTestUtility.env_vars_present():
        return print("aborting...")

    click.echo(f'Running tests for {",".join(targets) or "all"} targets')

    build_sys = plans.Options[plan_type.lower()](claims_dir)
    test_cases = build_sys.build_node_labels(targets)

    test.PyTestUtility.invoke_cases(test_cases, 'local')

@cli.command('smoke')
@click.argument('targets', nargs = -1)
@click.option('-p', '--plan_type', default = 'default',
    type = click.Choice([*plans.Options], case_sensitive = False))
@click.option('-c', '--claims_dir', default = 'test_claims')
def ExecSmokeTest(targets, plan_type, claims_dir):
    click.echo(f'Running smoke tests for {",".join(targets) or "all"} targets')

    build_sys = plans.Options[plan_type.lower()](claims_dir)
    test_cases = build_sys.build_node_labels(targets)

    test.PyTestUtility.invoke_cases(test_cases, 'staging')
