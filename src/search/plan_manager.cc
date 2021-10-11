#include "plan_manager.h"

#include "task_proxy.h"

#include "task_utils/task_properties.h"
#include "utils/logging.h"

#include <fstream>
#include <iostream>
#include <sstream>


using namespace std;

int calculate_plan_cost(const Plan &plan, const TaskProxy &task_proxy) {
    OperatorsProxy operators = task_proxy.get_operators();
    int plan_cost = 0;
    for (OperatorID op_id : plan) {
        plan_cost += operators[op_id].get_cost();
    }
    return plan_cost;
}

PlanManager::PlanManager()
    : plan_filename("sas_plan"),
      num_previously_generated_plans(0),
      is_part_of_anytime_portfolio(false) {
}

void PlanManager::set_plan_filename(const string &plan_filename_) {
    plan_filename = plan_filename_;
}

void PlanManager::set_state_filename(const string &state_filename_) {
    state_filename = state_filename_;
}

void PlanManager::set_num_previously_generated_plans(int num_previously_generated_plans_) {
    num_previously_generated_plans = num_previously_generated_plans_;
}

void PlanManager::set_is_part_of_anytime_portfolio(bool is_part_of_anytime_portfolio_) {
    is_part_of_anytime_portfolio = is_part_of_anytime_portfolio_;
}

void PlanManager::save_plan(
    const Plan &plan, const TaskProxy &task_proxy,
    bool generates_multiple_plan_files) {
    ostringstream filename;
    filename << plan_filename;
    ostringstream filename_state;
    filename_state << state_filename;
    int plan_number = num_previously_generated_plans + 1;
    if (generates_multiple_plan_files || is_part_of_anytime_portfolio) {
        filename << "." << plan_number;
    } else {
        assert(plan_number == 1);
    }
    ofstream outfile(filename.str());
    if (outfile.rdstate() & ofstream::failbit) {
        cerr << "Failed to open plan file: " << filename.str() << endl;
        utils::exit_with(utils::ExitCode::SEARCH_INPUT_ERROR);
    }
    OperatorsProxy operators = task_proxy.get_operators();
    for (OperatorID op_id : plan) {
        cout << operators[op_id].get_name() << " (" << operators[op_id].get_cost() << ")" << endl;
        outfile << "(" << operators[op_id].get_name() << ")" << endl;
    }
    int plan_cost = calculate_plan_cost(plan, task_proxy);
    bool is_unit_cost = task_properties::is_unit_cost(task_proxy);
    outfile << "; cost = " << plan_cost << " ("
            << (is_unit_cost ? "unit cost" : "general cost") << ")" << endl;
    outfile.close();

    ofstream outfile_state(filename_state.str());
    if (outfile_state.rdstate() & ofstream::failbit) {
        cerr << "Failed to open plan file: " << filename_state.str() << endl;
        utils::exit_with(utils::ExitCode::SEARCH_INPUT_ERROR);
    }

    utils::g_log << " i am quim " << endl;
    utils::g_log << " state init " << endl;
    auto init =  task_proxy.get_initial_state() ;
    auto s1 = init.get_unregistered_successor( operators[plan[0]] );
    auto s2 = s1.get_unregistered_successor( operators[plan[1]] );

    auto s =  task_proxy.get_initial_state() ;
    int it = 0;
    std::cout << "s " << it << std::endl;
    outfile_state << "s " << it << std::endl;
    task_properties::dump_pddl(s);
    task_properties::dump_pddl_to(s,outfile_state);

    for (OperatorID op_id : plan) {
      it++;
      s = init.get_unregistered_successor( operators[op_id] );
      std::cout << "s " << it << std::endl;
      outfile_state << "s " << it << std::endl;
      task_properties::dump_pddl(s);
      task_properties::dump_pddl_to(s,outfile_state);
    }
    std::cout  << std::endl;
    outfile_state << std::endl;


    // std::cout << "init " << std::endl;
    // task_properties::dump_pddl(init);
    // std::cout << "s1 " << std::endl;
    // task_properties::dump_pddl(s1);
    // std::cout << "s2 " << std::endl;
    // task_properties::dump_pddl(s2);

    // task_properties::dump_pddl( task_proxy.get_goals() );

    utils::g_log << "Plan length: " << plan.size() << " step(s)." << endl;
    utils::g_log << "Plan cost: " << plan_cost << endl;
    ++num_previously_generated_plans;
}
