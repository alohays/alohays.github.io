"""Independent numerical and source-wiring checks for the intelligence essay.

Uses only the standard library. It validates the toy calculations, the data
transcribed from cited sources, and the post's active figures and footnotes.
It does not claim to prove the cited theorems or validate a new intelligence metric.
"""
from pathlib import Path
from collections import Counter
import json
import math
import re
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
POST = ROOT / 'docs/blog/posts/physical-units-of-intelligence.md'
DATA = json.loads((HERE / 'energy-data.json').read_text())
checks = []


def check(name, condition, detail):
    if not condition:
        raise AssertionError(f'{name}: {detail}')
    checks.append({'check': name, 'detail': detail})


thermal = DATA['boltzmann_joule_per_kelvin'] * DATA['temperature_kelvin']
reset = thermal * math.log(2)
check('300 K unbiased-bit reset', math.isclose(reset, 2.870978885078724e-21, rel_tol=1e-12), reset)
for op in DATA['biology']['operations']:
    bound = thermal * math.log(op['alphabet_size'])
    ratio = op['estimated_joules'] / bound
    check(f'{op["label"]} bound', math.isclose(bound, op['reported_bound_joules'], rel_tol=.001),
          {'calculated_joules': bound, 'source_joules_rounded': op['reported_bound_joules']})
    check(f'{op["label"]} ratio', math.isclose(ratio, op['reported_ratio_approx'], rel_tol=.025), ratio)
ops = DATA['hardware']['operations']
check('Hardware source transcription',
      [(o['low_pj'], o['high_pj']) for o in ops] == [(0.1, 0.1), (4, 4), (10, 10), (20, 20), (100, 100), (1300, 2600)],
      'Compared to Horowitz accompanying presentation, slide 32; DRAM is a rough range, not a confidence interval.')
check('DRAM/add per-event ratio',
      [ops[-1][key] / ops[0]['low_pj'] for key in ['low_pj', 'high_pj']] == [13000, 26000],
      '13,000–26,000, with different operation widths explicitly retained.')
brain = DATA['illustrative_brain_arithmetic']
per_behaviour_bit = brain['power_watts'] / brain['behavioural_bits_per_second']
check('Illustrative brain arithmetic',
      per_behaviour_bit == 2 and 6.9e20 < per_behaviour_bit / reset < 7.1e20,
      {'joules_per_behavioural_bit': per_behaviour_bit, 'reset_floor_multiple': per_behaviour_bit / reset,
       'interpretation': 'Different measurement levels; not a physical reset cost or cross-agent efficiency ranking.'})

horizon = lambda p: math.log(.5) / math.log(p)
for p in [.159, .5, .9, .99, .999]:
    h = horizon(p)
    check(f'Toy horizon inversion, p={p}', math.isclose(p ** h, .5, rel_tol=1e-12), h)
    n = math.floor(h)
    check(f'Whole-step threshold, p={p}', p ** n >= .5 and p ** (n + 1) < .5,
          {'steps': n, 'success_at_n': p ** n, 'success_at_next': p ** (n + 1)})
for b in [.25, 1, 3, 7]:
    eps = 2 ** -b
    slope = math.log(2) * eps / ((1 - eps) * (-math.log(1 - eps)))
    delta = 1e-5
    plus = math.log(horizon(1 - 2 ** -(b + delta)))
    minus = math.log(horizon(1 - 2 ** -(b - delta)))
    numeric = (plus - minus) / (2 * delta)
    check(f'Former kappa is a semi-elasticity, b={b}', math.isclose(slope, numeric, rel_tol=1e-6),
          {'per_bit': slope, 'true_elasticity_in_b': b * slope})
for name, ratio in [('exact', horizon(.56) / horizon(.159)), ('asymptotic', (1 - .159) / (1 - .56))]:
    exponent = math.log(ratio) / math.log(250)
    multiplier = 2 ** (1 / exponent)
    check(f'Sampling extrapolation ({name})', math.isclose(multiplier ** exponent, 2, rel_tol=1e-12),
          {'hypothetical_horizon_ratio': ratio, 'sample_exponent': exponent,
           'projected_compute_multiplier_for_doubling': multiplier,
           'unvalidated_assumptions': 'Task coverage used as per-step success; two-point power law extrapolated.'})

# Exhaust all four states and all deterministic decision rules. No sampling.
states = [(colour, weight) for colour in [0, 1] for weight in [0, 1]]
channels = {'camera': lambda s: s[0], 'scale': lambda s: s[1],
            'camera_copy': lambda s: (s[0], s[0]), 'both': lambda s: s}
for name, channel in channels.items():
    observations = Counter(channel(s) for s in states)
    info = -sum((n / 4) * math.log2(n / 4) for n in observations.values())
    accuracies = []
    for target in [0, 1]:
        correct = sum(max(sum(channel(s) == obs and s[target] == decision for s in states)
                          for decision in [0, 1]) for obs in observations)
        accuracies.append(correct / 4)
    expected = {'camera': (1, [1, .5]), 'scale': (1, [.5, 1]),
                'camera_copy': (1, [1, .5]), 'both': (2, [1, 1])}[name]
    check(f'Parcel example: {name}', (info, accuracies) == expected,
          {'bits_about_world': info, 'colour_weight_optimal_accuracy': accuracies})

text = POST.read_text()
# Strip definitions before finding uses; each reference must actually be used.
defs = re.findall(r'^\[\^([^\]]+)\]:', text, re.M)
prose = re.sub(r'^\[\^[^\]]+\]:.*$', '', text, flags=re.M)
uses = set(re.findall(r'\[\^([^\]]+)\]', prose))
check('Footnotes resolve', len(defs) == len(set(defs)) and uses == set(defs),
      {'definitions': len(defs), 'uses': len(uses), 'missing': sorted(uses - set(defs)), 'unused': sorted(set(defs) - uses)})
draft = '\ndraft: true\n' in text
history = re.search(r'^## Changelog\s*$', text, re.M) is not None
check('Publication state and history agree',
      (draft and not history) or ('\ndraft: false\n' in text and history),
      {'draft': draft, 'public_history': history})
check('No unfinished markers', not re.search(r'\b(?:TODO|TBD|FIXME|VERIFY)\b', text), 'No drafting placeholders.')
check('No em dashes in post', '\u2014' not in text, 'Preserves the author\'s existing punctuation preference.')
active_figures = re.findall(r'--8<-- "([^"]+)"', text)
for rel in active_figures:
    p = ROOT / rel
    root = ET.parse(p).getroot()
    expected_role = 'group' if p.suffix == '.html' else 'img'
    check(f'Figure semantics: {p.name}', root.attrib.get('role') == expected_role and bool(root.attrib.get('aria-label')),
          {'viewBox': root.attrib.get('viewBox'), 'bytes': p.stat().st_size})
for rel in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
    if not rel.startswith(('https:', 'http:')):
        check(f'Image resolves: {Path(rel).name}', (POST.parent / rel).resolve().is_file(), rel)

result = {'status': 'passed', 'checks': checks, 'active_figure_count': len(active_figures),
          'scope': 'Numerical and artifact checks; primary-paper scope and editorial claims require the accompanying audit record.'}
report = ROOT / '_workspace/physical-units-checks/audit-results.json'
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(f'PASS: {len(checks)} checks; {len(active_figures)} active figures; {len(defs)} references.')
print(f'Wrote {report}')
