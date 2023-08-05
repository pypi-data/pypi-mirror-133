from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from typing import Dict, List
from pollination.honeybee_energy.simulate import SimulateModel


# input/output alias
from pollination.alias.inputs.model import hbjson_model_input
from pollination.alias.inputs.ddy import ddy_input
from pollination.alias.inputs.simulation import energy_simulation_parameter_input, \
    idf_additional_strings_input, measures_input


@dataclass
class CustomEnergySimEntryPoint(DAG):
    """Custom energy sim entry point."""

    # inputs
    model = Inputs.file(
        description='An energy Model as either a HBJSON, OSM, or IDF.',
        extensions=['hbjson', 'json', 'osm', 'idf'],
        alias=hbjson_model_input
    )

    epw = Inputs.file(
        description='EPW weather file to be used for the energy simulation.',
        extensions=['epw']
    )

    ddy = Inputs.file(
        description='A DDY file with design days to be used for the initial '
        'sizing calculation.', extensions=['ddy'],
        alias=ddy_input
    )

    sim_par = Inputs.file(
        description='SimulationParameter JSON that describes the settings for the '
        'simulation.', path='sim-par.json', extensions=['json'], optional=True,
        alias=energy_simulation_parameter_input
    )

    measures = Inputs.folder(
        description='A folder containing an OSW JSON be used as the base for the '
        'execution of the OpenStuduo CLI. This folder must also contain all of the '
        'measures that are referenced within the OSW.', path='measures', optional=True,
        alias=measures_input
    )

    additional_string = Inputs.str(
        description='An additional text string to be appended to the IDF before '
        'simulation. The input should include complete EnergyPlus objects as a '
        'single string following the IDF format. This input can be used to include '
        'EnergyPlus objects that are not currently supported by honeybee.', default='',
        alias=idf_additional_strings_input
    )

    # tasks
    @task(template=SimulateModel)
    def run_simulation(
        self, model=model, epw=epw, ddy=ddy, sim_par=sim_par,
        measures=measures, additional_string=additional_string
    ) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.idf, 'to': 'model.idf'},
            {'from': SimulateModel()._outputs.sql, 'to': 'eplusout.sql'},
            {'from': SimulateModel()._outputs.zsz, 'to': 'epluszsz.csv'},
            {'from': SimulateModel()._outputs.html, 'to': 'eplustbl.htm'},
            {'from': SimulateModel()._outputs.err, 'to': 'eplusout.err'}
        ]

    # outputs
    idf = Outputs.file(
        source='model.idf', description='The IDF model used in the simulation.'
    )

    sql = Outputs.file(
        source='eplusout.sql',
        description='The result SQL file output by the simulation.'
    )

    zsz = Outputs.file(
        source='epluszsz.csv', description='The result CSV with the zone loads '
        'over the design day output by the simulation.', optional=True
    )

    html = Outputs.file(
        source='eplustbl.htm',
        description='The result HTML page with summary reports output by the simulation.'
    )

    err = Outputs.file(
        source='eplusout.err',
        description='The error report output by the simulation.'
    )
