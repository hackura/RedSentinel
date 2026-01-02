from redsentinel.simulator import run_simulation

def test_run_simulation_returns_result():
    """
    Ensure the simulator runs without crashing
    and returns a result object.
    """
    result = run_simulation("example.com")

    assert result is not None
    assert isinstance(result, dict)
