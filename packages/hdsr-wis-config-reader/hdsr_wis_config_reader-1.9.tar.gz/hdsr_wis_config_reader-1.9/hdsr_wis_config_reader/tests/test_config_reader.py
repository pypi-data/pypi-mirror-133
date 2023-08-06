from hdsr_wis_config_reader.tests.fixtures import fews_config_github
from hdsr_wis_config_reader.tests.fixtures import fews_config_local

import logging
import pandas as pd


# silence flake8
fews_config_local = fews_config_local
fews_config_github = fews_config_github

logger = logging.getLogger(__name__)


expected_parameters = [
    "A",
    "A.15",
    "AREA",
    "B.d",
    "B.m",
    "B.y",
    "BG.A",
    "BG.V.tot",
    "BG.b.0",
    "BG.fd.0",
    "BG.ka.0",
    "BG.o.0",
    "BG.tot.0",
    "BGf.tot",
    "BegFD.a",
    "BegFD.s",
    "BegKl",
    "BegKrA.a",
    "BegKrA.s",
    "BegOnd.a",
    "BegOnd.s",
    "BegOpv.a",
    "BegOpv.s",
    "BegOvs.a",
    "BegTot.a",
    "BegTot.s",
    "C.0",
    "C.15",
    "C2.0",
    "CF",
    "CTS_M_GMT+01:00",
    "CTS_Y_GMT+01:00",
    "DD.15",
    "DD.AA.m",
    "DD.AD.m",
    "DD.AM.m",
    "DD.AR.m",
    "DD.AU.m",
    "DD.d",
    "DD.h",
    "DD.m",
    "DDH.15",
    "DDH.d",
    "DDH.h",
    "DDH.m",
    "DDHM.d",
    "DDL.15",
    "DDL.d",
    "DDL.h",
    "DDL.m",
    "DDLM.d",
    "DDM.d",
    "DDU.d",
    "DIFF",
    "DMaai.0",
    "DRAAIDUUR_DAY1",
    "DRAAIDUUR_DAY2",
    "DRAAIDUUR_DAY3",
    "DRAAIDUUR_DAY4",
    "DRAAIDUUR_UUR_CUM",
    "DRAAIDUUR_UUR_NONCUM",
    "DZm.0",
    "DaysOld.d",
    "DaysOld.m",
    "DaysOld.w",
    "DaysOld.y",
    "DbAug1.a",
    "ES.0",
    "ES.15",
    "ES2.0",
    "ES2.15",
    "EV.15",
    "EV.m",
    "Eact.d",
    "Eact.m",
    "Eact.y",
    "Edef.C.d",
    "Edef.d",
    "Edef.m",
    "Edef.y",
    "EowF",
    "Epot.d",
    "Epot.m",
    "Epot.y",
    "Eref.d",
    "Eref.m",
    "Eref.y",
    "F.0",
    "F.15",
    "F.AA.m",
    "F.AD.m",
    "F.AM.m",
    "F.AR.m",
    "F.AU.m",
    "F.d",
    "F.h",
    "F.m",
    "FRC",
    "G.dino",
    "GFG",
]

expected_df_parameter_column_names = [
    "DESCRIPTION",
    "GROUP",
    "ID",
    "NAME",
    "PARAMETERTYPE",
    "SHORTNAME",
    "UNIT",
    "USESDATUM",
    "VALUERESOLUTION",
]


def test_local_fews_config(fews_config_local):
    fews_config = fews_config_local
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets
    for loc_set in loc_sets:
        try:
            fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            logger.error(f"got error in get_locations() for loc_set {loc_set}, err={err}")

    df_parameters = fews_config_local.get_parameters()
    assert isinstance(df_parameters, pd.DataFrame)
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names


def test_github_fews_config_prd(fews_config_github):
    fews_config = fews_config_github
    fews_config.MapLayerFiles  # noqa
    fews_config.RegionConfigFiles  # noqa
    fews_config.IdMapFiles  # noqa
    loc_sets = fews_config.location_sets
    for loc_set in loc_sets:
        try:
            fews_config.get_locations(location_set_key=loc_set)
        except Exception as err:
            logger.error(f"got error in get_locations() for loc_set {loc_set}, err={err}")

    df_parameters = fews_config_github.get_parameters()
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names
    assert len(df_parameters) > 100
    assert sorted(df_parameters.columns) == expected_df_parameter_column_names
