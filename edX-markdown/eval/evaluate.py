from make_params import make_params
from find_matches import find_matches
from find_matches_w_variables import find_matches_w_variables


def get_numerical_answer(eval_tree):
    """Get the final value from and evaluation tree"""
    if type(eval_tree[0])==list:
        return eval_tree[0][1]
    else:
        return eval_tree[1]


def check_w_tol(ans, att, tol):
	if ans == 0:
		if att == 0:
			return True
		else:
			return False
	else:
		ratio = float(att)/ans
		if ratio < tol and ratio > (1/tol):
			return True
		else:
			return False


def evaluate(ans, att, tol = 1+1e-5):
	ans = ans.strip("\[")
  	ans = ans.strip("\]")
  	ans = ans.replace("{","")
  	ans = ans.replace("}","")
  	att = att.strip("'")
	p = make_params(ans, att)
	if p == {}:
		return False
	att_value = get_numerical_answer(p['att_tree'])
	ans_value = get_numerical_answer(p['ans_tree'])
	final_pairs = find_matches(p, tol)

	if len(final_pairs) == 1 and final_pairs[0][0] == 'R':
		return True
	else:
		return check_w_tol(ans_value, att_value, tol)


def evaluate_w_variables(ans, att, variable_values, test_all=False):
	ans = ans.strip("\[")
  	ans = ans.strip("\]")
  	ans = ans.replace("{","")
  	ans = ans.replace("}","")
  	att = att.strip("'")
	matches = find_matches_w_variables(ans, att, variable_values, test_all)
	if matches and len(matches) == 1 and matches[0][0] == 'R':
		return True
	else:
		return False