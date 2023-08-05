# -*- coding: utf-8 -*-
"""
when behave run scenario will trigger this
"""
import traceback

import flybird.core.global_resource as gr
import flybird.utils.language_helper as lge
from flybird.core.global_context import GlobalContext
from flybird.core.driver import screen
from flybird.utils import flybird_log as log
from flybird.utils import launch_helper


def scenario_init(context, scenario):
    """
    init description and screen record
    """
    # initialize the description
    # the information added to the description will
    # take effect in this scenario
    scenario.description.append("initialization description_")
    # Initialize the sequence of steps to be executed
    # which is required for subsequent associated screenshots
    context.cur_step_index = 0
    # Whether to start recording screen
    # it is convenient to have screen recording information
    # associated in the report when it fails
    context.scenario_screen_record = False
    # Restart the app before running
    launch_helper.app_start("before_run_page")
    if gr.get_flow_behave_value("fail_screen_record", True):
        no_screen_record_step = True
        for step in scenario.all_steps:
            if step.name.strip().startswith(
                    lge.parse_glb_str(
                        "start record",
                        scenario.feature.language
                    )
            ) or step.name.strip().startswith(
                lge.parse_glb_str("stop record", scenario.feature.language)
            ):
                no_screen_record_step = False
                break
        if no_screen_record_step:
            try:
                screen_record = gr.get_value("screenRecord")
                timeout = gr.get_flow_behave_value(
                    "scenario_screen_record_time", 120
                )
                screen_record.start_record(timeout)
                context.scenario_screen_record = True
            except Exception as scenario_error:
                log.error(
                    f"Running scene: An error occurred when starting to "
                    f"record the screen before {scenario.name}"
                    f", error: {str(scenario_error)}"
                )


def scenario_fail(context, scenario):
    """
    scenario fail handler
    """
    log.info(
        f"feature:{scenario.feature.name} scenario:{scenario.name}"
        f" failed to run"
    )
    need_copy_record = 0

    # the scene fails to output a log and take a screenshot
    for step in scenario.all_steps:
        if step.name.strip().startswith(
                lge.parse_glb_str("start record", scenario.feature.language)
        ):
            need_copy_record += 1
        elif step.name.strip().startswith(
                lge.parse_glb_str("stop record", scenario.feature.language)
        ):
            need_copy_record -= 1
        if step.status == "failed":
            info_log = f"step:{step.name}"
            log.info(info_log)
            log.error(step.error_message)
            log.info("failed screenshot")
            screen.screen_link_to_behave(
                scenario, context.cur_step_index - 1, "fail_"
            )
            break

    # save screen recording
    if need_copy_record >= 1 or context.scenario_screen_record:
        screen_record = gr.get_value("screenRecord")
        screen_record.stop_record()
        screen_record.link_record(scenario, context.cur_step_index - 1)

    # the processing of the current page after the scene fails
    launch_helper.app_start("scenario_fail_page")
    scenario_screen_record_str = str(context.scenario_screen_record)
    log.info(
        f"scenario_fail, need_copy_record: {str(need_copy_record)},"
        f" context.scenario_screen_record: {scenario_screen_record_str}"
    )


def scenario_success(context, scenario):
    """
    scenario success handler
    """
    # adjustment of the currently displayed page after the scene is successful
    if context.scenario_screen_record:
        screen_record = gr.get_value("screenRecord")
        screen_record.stop_record()

    launch_helper.app_start("scenario_success_page")


class OnBefore:  # pylint: disable=too-few-public-methods
    """
    before run scenario will trigger this
    """

    name = "OnBefore"
    order = 5

    @staticmethod
    def can(context, scenario):
        return True

    @staticmethod
    def run(context, scenario):
        """
        write run info into description,it will be used at reporter
        """
        try:
            f_name = scenario.feature.name
            log.info(
                f"running feature:{f_name} scenario:{scenario.name},"
                f" location: {scenario.feature.location}"
            )
            scenario_init(context, scenario)
            data = launch_helper.get_runtime_data(scenario)
            scenario.description.append(data)

        except Exception:
            traceback.print_exc()

        # hook extend by tester
        before_scenario_extend = launch_helper.get_hook_file(
            "before_scenario_extend"
        )
        if before_scenario_extend is not None:
            before_scenario_extend(context, scenario)


class OnAfter:  # pylint: disable=too-few-public-methods
    """
    scenario after event
    """

    name = "OnAfter"
    order = 100

    @staticmethod
    def can(context, scenario):
        return True

    @staticmethod
    def run(context, scenario):
        """
        exe scenario after
        """
        try:
            if scenario.status == "failed":
                scenario_fail(context, scenario)
            else:
                scenario_success(context, scenario)
        except Exception:
            traceback.print_exc()

        # if there is a hook custom behavior, call the related function
        after_scenario_extend = launch_helper.get_hook_file(
            "after_scenario_extend"
        )
        if after_scenario_extend is not None:
            after_scenario_extend(context, scenario)


# add scenario event to global processor
var = GlobalContext.join("before_scenario_processor", OnBefore, 1)
var1 = GlobalContext.join("after_scenario_processor", OnAfter, 1)
