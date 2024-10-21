import pytest
from potatofarm import Plot
from potatofarm import Bank
from potatofarm import getdifficulty
from potatofarm import start
from potatofarm import potato_yield
from potatofarm import dec_quality
from potatofarm import shop
from potatofarm import goal


def test_getdifficulty(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'e')
    dim, first = getdifficulty()
    assert dim == 1
    assert first == 100

    monkeypatch.setattr('builtins.input', lambda _: 'NORMAL')
    dim, first = getdifficulty()
    assert dim == 1.1
    assert first == 80

    monkeypatch.setattr('builtins.input', lambda _: 'hard')
    dim, first = getdifficulty()
    assert dim == 1.2
    assert first == 50


def test_start(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '120')
    terminal = start()
    assert terminal == 120


    inputs = iter(['ff', '', '0.....', '990.8   '])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    terminal = start()
    assert terminal == 990


def test_potato_yield():
    plott = Plot()
    account = Bank(100)
    for _ in range(100):
        amount = potato_yield(account, plott)
        assert 0 < amount <= 10
    for x in range (2):
        plott.lv += 1
        for _ in range(100):
            amount = potato_yield(account, plott)
            assert 0 < amount <= 10 + (x+1)*5


def test_dec_quality():
    plott = Plot()
    plots = []
    plots.append(plott)
    dec_quality(plots, 1)
    assert plott.nutrients < 1
    testa = plott.nutrients
    assert plott.pest_control < 1
    testb = plott.pest_control
    assert plott.maintenance< 1
    testc = plott.maintenance
    dec_quality(plots, 1)
    assert plott.nutrients < testa
    assert plott.pest_control < testb
    assert plott.maintenance < testc


def test_shop(monkeypatch):
    plott = Plot()
    account = Bank(200)
    plots = []
    plots.append(plott)
    dec_quality(plots, 1)
    dec_quality(plots, 1)

    monkeypatch.setattr('builtins.input', lambda _: '1')
    shop(plott, account)
    assert plott.nutrients == 1

    monkeypatch.setattr('builtins.input', lambda _: '2')
    shop(plott, account)

    monkeypatch.setattr('builtins.input', lambda _: '3')
    shop(plott, account)
    assert plott.pest_control == 1
    assert plott.maintenance == 1

    monkeypatch.setattr('builtins.input', lambda _: '4')
    shop(plott, account)
    assert plott.lv == 2


def test_shopmoney(monkeypatch):
    plott = Plot()
    account = Bank(0)
    plots = []
    plots.append(plott)
    dec_quality(plots, 1)
    dec_quality(plots, 1)

    monkeypatch.setattr('builtins.input', lambda _: '1')
    shop(plott, account)
    assert plott.nutrients < 1

    monkeypatch.setattr('builtins.input', lambda _: '2')
    shop(plott, account)
    monkeypatch.setattr('builtins.input', lambda _: '3')
    shop(plott, account)
    assert plott.pest_control < 1
    assert plott.maintenance < 1

    monkeypatch.setattr('builtins.input', lambda _: '4')
    shop(plott, account)
    assert plott.lv == 1


def test_goal(monkeypatch):
    account = Bank(150)
    terminal = 120
    season = 3
    freeplay = 0
    start_time = 0

    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with pytest.raises(SystemExit): goal(account, terminal, season, freeplay, start_time)

    inputs = ['n', '', 'kjrewjo']
    for user_input in inputs:
        monkeypatch.setattr('builtins.input', lambda _: user_input)
        result = goal(account, terminal, season, freeplay, start_time)
        assert result == 1
