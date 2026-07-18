from econlab.model import EconomyModel, Shock


def test_model_runs_and_collects_data() -> None:
    model = EconomyModel(n_households=50, n_firms=5, seed=1)
    for _ in range(5):
        model.step()

    frame = model.datacollector.get_model_vars_dataframe()
    assert len(frame) == 6
    assert frame["unemployment_rate"].between(0, 1).all()


def test_transfer_is_active_only_during_shock_window() -> None:
    model = EconomyModel(
        n_households=20,
        n_firms=2,
        seed=2,
        shock=Shock(start=2, end=3, transfer=1.0),
    )
    model.step()
    assert model.current_transfer == 0.0
    model.step()
    assert model.current_transfer == 1.0
    model.step()
    assert model.current_transfer == 1.0
    model.step()
    assert model.current_transfer == 0.0
