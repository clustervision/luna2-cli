#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This code is part of the TrinityX software suite
# Copyright (C) 2026  ClusterVision Solutions b.v.

"""
`luna boot status` reads a node's install state and places it on a ladder.

Every bar in the view divides by a count of nodes at or past a stage, so a state
the ladder does not recognise is not a visible error - it is a node quietly missing
from every bar, which reads as a smaller cluster rather than as a bug. That is the
failure this file exists to make impossible to merge.

The states are the daemon's, listed in daemon/utils/monitor.py. They are named here
because the two repos cannot import each other; the pairing is what the daemon-side
test on the install templates holds up from the other end.
"""

import logging

import pytest

import luna.utils.log as luna_log
from luna.boot import Boot


@pytest.fixture(autouse=True)
def _stub_logger():
    """A logger without Log.init_log()'s root-only file handler."""
    previous = luna_log.Log._Log__logger  # noqa: SLF001 - name-mangled by design
    luna_log.Log._Log__logger = logging.getLogger('luna2-cli-tests')  # noqa: SLF001
    yield
    luna_log.Log._Log__logger = previous  # noqa: SLF001


# daemon/utils/monitor.py, node_state[204], plus the three lpart phases the lpart
# template builds at run time from install.lpart.${LUNAPHASE}
DAEMON_STATES = (
    'install.discovered', 'install.rendered', 'install.downloaded', 'install.started',
    'install.completed', 'install.scripts', 'install.prescript', 'install.setupbmc',
    'install.partscript', 'install.lpart.pre', 'install.lpart.part', 'install.lpart.post',
    'install.download', 'install.unpack', 'install.setnet', 'install.secrets',
    'install.postscript', 'install.roles', 'install.profiles', 'install.image',
    'install.finalizing', 'install.success', 'install.booted',
)

# deliberately off the ladder: an error is not a position in a boot, and
# lpart_unavailable is a warning the next step overwrites - the node carries on down
# the classic path and reports download and unpack from there
NOT_A_STAGE = ('install.error', 'install.lpart_unavailable')


@pytest.fixture(name='boot')
def boot_fixture():
    """The class without its constructor, which builds an argument parser."""
    return Boot.__new__(Boot)


def test_every_state_the_daemon_can_send_lands_on_the_ladder(boot):
    """A state nobody placed makes a node vanish from every bar."""
    missing = [state for state in DAEMON_STATES if boot.node_stage(state) is None]
    assert not missing, f'no stage for: {missing}'


def test_a_state_matches_one_stage_and_not_two(boot):
    """
    Matching is on a substring of the state, so a step named inside another one
    would place a node twice and the first hit would win silently. partscript and
    lpart.part are the pair that nearly collide.
    """
    for state in DAEMON_STATES:
        lowered = state.lower()
        hits = [name for name, steps, _ in boot.BOOT_STAGES
                if any(step in lowered for step in steps)]
        assert len(hits) == 1, f'{state} matches {hits}'


def test_the_states_left_off_the_ladder_are_the_ones_we_meant(boot):
    """Off the ladder is a decision, so it is pinned rather than assumed."""
    for state in NOT_A_STAGE:
        assert boot.node_stage(state) is None, f'{state} unexpectedly has a stage'


def test_the_lpart_phases_sit_where_the_classic_steps_sit(boot):
    """
    lpart runs the same install as three phases of its own. pre belongs with the
    preparation, part carries the image so it belongs with unpack, post finalises
    the bootloader and belongs with the configuration. Get this wrong and an lpart
    cluster reports progress it has not made.
    """
    stage = lambda state: boot.BOOT_STAGES[boot.node_stage(state)][0]
    assert stage('install.lpart.pre') == stage('install.prescript') == 'prepare'
    assert stage('install.lpart.part') == stage('install.unpack') == 'unpack'
    assert stage('install.lpart.post') == stage('install.postscript') == 'configure'


def test_progress_never_goes_backwards_along_the_ladder(boot):
    """The total bar is a mean of these, so a dip makes a boot look like it reversed."""
    weights = [weight for _, _, weight in boot.BOOT_STAGES]
    assert weights == sorted(weights), weights
    assert weights[-1] == 100


def test_a_step_that_runs_before_download_scores_less_than_download(boot):
    """
    The steps are not in the order they are declared in: scripts, prescript, bmc and
    partscript all run BEFORE the image is fetched. Scoring them above download makes
    a node three minutes into a boot read as nearly finished.
    """
    for early in ('install.prescript', 'install.setupbmc', 'install.partscript'):
        assert boot.step_progress(early) < boot.step_progress('install.download'), early


def test_the_milestones_descend_and_name_a_real_stage(boot):
    """
    Each bar counts nodes at or past a stage, so the thresholds have to rise and the
    counts therefore fall. A threshold off the end of the ladder counts nobody, ever.
    """
    thresholds = [threshold for _, threshold, _ in boot.BOOT_MILESTONES]
    assert thresholds == sorted(thresholds)
    assert max(thresholds) == len(boot.BOOT_STAGES) - 1
    assert min(thresholds) == 0
