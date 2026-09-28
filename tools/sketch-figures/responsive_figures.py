"""Build the essay's English responsive figure snippets.

Run after responsive_plots.py. All explanatory text is HTML, with no fixed
height or SVG text coordinates. Existing numerical values and caveats are kept.
Use --korean-review to also build local translations in the ignored workspace.
"""
import argparse
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/assets/images/blog/physical-units'
KO_OUT = ROOT / '_workspace/2026-09-20-self-contained/figures'
LANG = 'en'

def L(en, ko): return ko if LANG == 'ko' else en
def div(cls, text): return f'<div class="pu-{cls}">{text}</div>'
def panel(title, content, tone='', label=''):
    return div('panel'+(' pu-'+tone if tone else ''), (div('label',label) if label else '')+div('panel-title',title)+content)
def copy(s): return div('copy',s)
def note(s): return div('note',s)
def footer(s): return div('footer',s)
def fig(name,title,subtitle,body,foot=''):
    return (f'<div class="pu-figure" data-visual-id="{name}" role="group" aria-label="{escape(title,quote=True)}" lang="{LANG}" markdown="0">'
            +div('title',title)+div('subtitle',subtitle)+div('body',body)+(footer(foot) if foot else '')+'</div>\n')
def ranks(names):
    return '<ol class="pu-ranks">'+''.join(f'<li><span class="pu-rank">{i}.</span><span class="pu-model">{n}</span></li>' for i,n in enumerate(names,1))+'</ol>'
def svg_plot(name, alt):
    s=(OUT/'plots'/f'{name}.svg').read_text()
    s=re.sub(r'aria-label="[^"]*"',f'aria-label="{escape(alt,quote=True)}"',s,count=1)
    return re.sub(r'\s+', ' ', s).strip()
def chart(name, alt, ylabel, xlabel):
    return div('chart',div('axis-label',ylabel)+svg_plot(name,alt)+div('axis-label',xlabel))
def measure(label,value,tone=''):
    return div('measure'+(' pu-'+tone if tone else ''),label+f'<strong>{value}</strong>')

def four_axes():
    cards=[
        ('01',L('Input','입력'),L('How much information can it take in and use?','얼마나 많은 정보를 받아 활용할 수 있나?'),'blue'),
        ('02',L('Output','출력'),L('How far and broadly can it look ahead?','얼마나 멀고 넓은 미래를 고려하나?'),'gold'),
        ('03',L('Multimodality','다중양식'),L('Which physical ranges can it reach, and how fast?','어떤 물리적 범위를 얼마나 빠르게 다루나?'),'purple'),
        ('04',L('Efficiency','효율'),L('How much energy and time does that capability need?','그 능력을 발휘하는 데 에너지와 시간이 얼마나 드나?'),'red')]
    return fig('four-axes',L('Four questions about intelligence','지능에 관한 네 가지 질문'),L('Four views of the same system.','같은 시스템을 바라보는 네 가지 관점.'),div('columns',''.join(panel(t,copy(c),color,n) for n,t,c,color in cards)))

def scoreboard():
    cards=[
        (L('Input capacity','입력 수용 능력'),'C',L('Scenario ranking','시나리오 순위'),['GPT-6 Astra','Claude Fable 5.1'],'blue',
         L('Context ceiling × an assumed usable fraction.','문맥 상한과 가정한 사용 가능 비율을 곱한 값.'),L('The public AA-LCR ranking differs.','공개 AA-LCR 순위와 다르다.')),
        (L('Future output','미래 출력 능력'),'F',L('Scenario ranking','시나리오 순위'),['GPT-6 Astra','Claude Fable 5.1'],'gold',
         L('Both have strong public evidence on agentic work.','둘 다 에이전트 작업에서 강한 공개 근거가 있다.'),L('The exact order comes from a prior; the future tree is untested.','정확한 순서는 사전값에서 나온다. 미래 나무 시험은 아직 하지 않았다.')),
        (L('Physical reach','물리적 도달 범위'),'M†',L('Proxy ranking','대리 지표 순위'),['Muse Spark 1.3','DeepSeek V4.1 Flash'],'purple',
         L('Video support and API response speed drive this proxy.','영상 지원과 API 응답 속도로 구성한 대리 지표.'),L('Physical information rates are unmeasured.','물리 정보율은 아직 측정하지 않았다.')),
        (L('Energy and time','에너지와 시간'),'η‡',L('Scenario ranking','시나리오 순위'),['DeepSeek V4.1 Flash','Qwen3.8 27B','Muse Spark 1.3'],'red',
         L('The order follows assumed energy values.','가정한 에너지 값에 따라 정해진 순서.'),L('These are not wattmeter readings.','전력계로 측정한 값이 아니다.'))]
    body=div('columns',''.join(panel(f'{symbol} · {title}',ranks(names)+copy(reason)+note(caution),color,label) for title,symbol,label,names,color,reason,caution in cards))
    return fig('provisional-scoreboard',L('Spoiler: AI ranked in bits and joules','스포일러: AI를 비트와 줄로 줄세워봤다'),
               L('Conditional rankings from the seven-model scenario.','일곱 모델에 가정을 대입해 얻은 조건부 순위.'),body,
               L('All four rankings need independent measurement. The table below gives the assumptions and values.','네 순위 모두 독립 측정이 필요하다. 본문 아래 표에 가정과 수치를 적었다.'))

def input_test():
    bits=div('bits',''.join(div('bit',f'{chr(65+i)}: {v}') for i,v in enumerate([1,0,0,1,1,1,0,1])))
    body=div('steps',
        panel(L('Read eight facts','정보 8개 읽기'),bits,'blue',L('Step 1','1단계'))+
        panel(L('Remove the input','입력 치우기'),div('number',L('10 seconds','10초'))+copy(L('Wait. The later question is still unknown.','기다린다. 나중에 무엇을 물을지는 아직 모른다.')),'',L('Step 2','2단계'))+
        panel(L('Answer a fresh query','새 질문에 답하기'),copy(L('Parcel F?','소포 F는?'))+div('number',L('Bay 1','하역장 1'))+note(L('Choose the query only now.','질문은 이때 고른다.')),'gold',L('Step 3','3단계')))
    return fig('input-test',L('Ask after the input is gone','입력이 사라진 뒤에 묻기'),L('Each destination is an independent binary fact.','각 목적지는 서로 독립적인 이진 정보다.'),body,L('Increase the number of facts. Keep presentation time, retention interval and response deadline fixed.','정보 수를 늘려가며 시험한다. 제시 시간, 유지 시간, 응답 기한은 고정한다.'))

def output_futures():
    body=panel(L('What the robot knows','로봇이 아는 것'),copy(L('Instructions, past observations and the current scene.','지시, 과거 관측, 현재 상황.')),'blue')
    body+=div('flow',L('↓ Consider the feasible alternatives','↓ 실행 가능한 대안들을 고려한다'))
    body+=div('columns',panel(L('Door open','문이 열려 있다'),copy(L('The short route is available.','짧은 경로로 갈 수 있다.')))+panel(L('Door closed','문이 닫혀 있다'),copy(L('Find another route.','다른 경로를 찾아야 한다.'))))
    body+=div('flow',L('↓ Produce a useful output','↓ 유용한 출력을 만든다'))
    body+=div('columns',panel(L('Prediction','예측'),copy(L('Arrival time, delays and risk to the parcel.','도착 시간, 지연, 소포가 손상될 위험.')),'gold')+panel(L('Action trajectory','행동 궤적'),copy(L('A sequence of feasible movements over time.','시간에 따라 이어지는 실행 가능한 움직임.')),'gold'))
    return fig('output-futures',L('Output includes actions','행동도 출력에 포함된다'),L('Goal: deliver the fragile parcel intact and on time.','목표: 깨지기 쉬운 소포를 제시간에 안전하게 배송하기.'),body,L('Either output can change when new information arrives. Both concern the consequences of feasible choices.','새 정보가 들어오면 두 출력 모두 달라질 수 있다. 둘 다 실행 가능한 선택의 결과를 다룬다.'))

def tree_svg(depth,branch):
    width,height=300,245
    levels=[[(12+(j+.5)*276/(branch**k),16+k*210/depth) for j in range(branch**k)] for k in range(depth+1)]
    path=[0]
    for k in range(1,depth+1): path.append(path[-1]*branch+(1 if k%2 else 0))
    parts=[]
    for k in range(1,depth+1):
        for j,(x,y) in enumerate(levels[k]):
            a,b=levels[k-1][j//branch];marked=j==path[k]
            parts.append(f'<line x1="{a}" y1="{b}" x2="{x}" y2="{y}" stroke="var(--pu-accent)" stroke-width="{3 if marked else 1}" opacity="{1 if marked else .45}" />')
    for k,level in enumerate(levels):
        for j,(x,y) in enumerate(level):
            parts.append(f'<circle cx="{x}" cy="{y}" r="{4 if k==depth else 5}" fill="var(--pu-accent)" opacity="{1 if j==path[k] else .55}" />')
    alt=L(f'{depth} levels, {branch} branches per node, 16 leaves. One path is highlighted.',f'깊이 {depth}, 지점당 분기 {branch}개, 말단 16개. 한 경로를 강조했다.')
    return f'<svg class="pu-tree" viewBox="0 0 {width} {height}" role="img" aria-label="{alt}">'+''.join(parts)+'</svg>'

def future_tree():
    body=div('columns',''.join(panel(L(f'{d} levels × {b} branches',f'깊이 {d} × 분기 {b}'),tree_svg(d,b)+div('result',L('16 paths = 4 bits','16개 경로 = 4비트'))) for d,b in [(4,2),(2,4)]))
    return fig('future-tree',L('Depth and width both count','깊이와 폭을 함께 측정하기'),L('Equally likely, distinct future cases.','확률이 같은, 서로 다른 미래 경우들.'),body,L('The information is equal; the difficulty need not be. Test both structures on fresh cases.','정보량은 같아도 난도는 다를 수 있다. 새 사례로 두 구조를 모두 시험한다.'))

def horizon():
    alt=L('Independent-step success model. 90% gives 6.6 steps; 99% gives 69.','단계별 성공이 독립인 모형. 성공률 90%는 6.6단계, 99%는 69단계다.')
    left=chart('horizon',alt,L('50% task horizon (steps, log scale)','성공률 50%인 작업 길이 (단계, 로그 척도)'),L('Success per step (%)','단계별 성공률 (%)'))
    right=div('measures',measure(L('90% success per step','단계별 성공률 90%'),L('6.6 steps','6.6단계'),'blue')+measure(L('99% success per step','단계별 성공률 99%'),L('69 steps','69단계'),'blue'))
    legend=div('legend','<span><i class="pu-key"></i>'+L('Exact model','정확한 모형')+'</span><span><i class="pu-key pu-key-dash"></i>'+L('High-reliability approximation','높은 신뢰도에서의 근사')+'</span>')
    return fig('kappa-curve',L('Small errors accumulate','작은 오류도 누적된다'),L('A calculation, not a measured agent horizon.','실제 에이전트 측정값이 아니라 계산 예시다.'),div('plot-pair',left+right)+legend,L('Independent steps. One failure ends the job. No recovery or retries.','단계별 성공은 독립이다. 한 번 실패하면 일이 끝나며 복구나 재시도는 없다.'))

def blackwell():
    boxes=div('parcels',''.join(div('parcel pu-'+tone,f'<strong>{color}</strong>{weight}') for tone,color,weight in [('red',L('Red','빨강'),L('Light','가벼움')),('red',L('Red','빨강'),L('Heavy','무거움')),('blue',L('Blue','파랑'),L('Light','가벼움')),('blue',L('Blue','파랑'),L('Heavy','무거움'))]))
    table='<table class="pu-table"><thead><tr>'+''.join(f'<th scope="col">{x}</th>' for x in [L('Observation','관측'),L('Colour?','색상은?'),L('Weight?','무게는?')])+'</tr></thead><tbody>'
    for name,c,w in [(L('Colour camera','색상 카메라'),'100%','50%'),(L('Scale','저울'),'50%','100%'),(L('Both','둘 다'),'100%','100%')]:
        table+=f'<tr><th scope="row">{name}</th><td>{c}</td><td>{w}</td></tr>'
    table+='</tbody></table>'
    return fig('blackwell-parcels',L('One bit of colour. One bit of weight.','색상 1비트. 무게 1비트.'),L('Four equally likely parcels. The attributes are independent.','확률이 같은 네 소포. 색상과 무게는 독립이다.'),boxes+div('result',L('Best possible accuracy in this example','이 예시에서 가능한 최고 정확도'))+table,L('Copying the camera feed adds no information about weight.','카메라 영상을 복사해도 무게에 관한 정보는 늘지 않는다.'))

def physical_ranges():
    body=''
    for title,labels,tone in [(L('Microscopic range','미시적 범위'),['1 µm','10 µm','100 µm','1 mm'],'blue'),(L('Macroscopic range','거시적 범위'),['1 km','10 km','100 km','1,000 km'],'gold')]:
        body+=div('scale',div('scale-head',f'<strong>{title}</strong><span>'+L('Weight 3','비중 3')+'</span>')+div('segments',''.join(f'<span class="pu-{tone}">10×</span>' for _ in range(3)))+div('ticks',''.join(f'<span>{v}</span>' for v in labels)))
    full=div('scale-head','<strong>'+L('Across the whole interval','전체 구간에 걸친 범위')+'</strong><span>'+L('Weight 12','비중 12')+'</span>')
    full+=div('segments pu-segments-wide',''.join('<span'+(' class="pu-blue"' if i<3 else ' class="pu-gold"' if i>=9 else '')+'></span>' for i in range(12)))
    full+=div('ticks','<span>1 µm</span><span>1,000 km</span>')+note(L('3 microscopic steps + 6 between + 3 macroscopic steps.','미시 구간 3칸 + 사이 구간 6칸 + 거시 구간 3칸.'))
    return fig('physical-ranges',L('One ruler across physical scales','서로 다른 규모에 같은 자를 대기'),L('Same quantity and relative precision. Each step is 10×.','같은 물리량과 상대 정밀도. 한 칸마다 10배.'),body+div('scale',full),L('A proposed reference map, not measured physical coverage. The reference can extend.','측정된 접근 범위가 아닌, 기준 지도 제안이다. 기준 범위는 확장할 수 있다.'))

def multimodal_rate():
    body=''
    for letter,a,b,score in [('A',100,0,100),('B',50,50,200),('C',200,0,200)]:
        regs=div('regions',div('region pu-blue',L('Region 1','영역 1')+f'<strong>{a} bit/s</strong>')+div('region'+(' pu-gold' if b else ''),L('Region 2','영역 2')+f'<strong>{b} bit/s</strong>'))
        summary=div('summary','<span>'+L('Total','합계')+f': {a+b} bit/s</span><strong>M = {score} bit/s</strong>')
        body+=div('case',div('case-letter',letter)+div('case-body',regs+summary))
    return fig('multimodal-rate',L('Same rate, different physical reach','같은 정보율, 다른 물리적 범위'),L('Reference weight: 1 in each region.','두 영역의 기준 비중은 각각 1이다.'),body,
               L('B scores twice A at the same total rate. B and C tie: breadth can offset speed. M includes that chosen tradeoff; it is not raw throughput.','B는 합계 정보율이 같은 A의 두 배 점수를 받는다. B와 C는 동점이다. M에는 범위와 속도의 교환 규칙이 들어 있으며 실제 총전송량과 다르다.'))

def efficiency():
    alt=L('A: 10 seconds and 1 joule. B: 1 second and 10 joules. C: 1 second and 1 joule.','A: 10초와 1줄. B: 1초와 10줄. C: 1초와 1줄.')
    plot=chart('energy-time',alt,L('Energy used (J)','사용 에너지 (J)'),L('Elapsed time (s)','경과 시간 (초)'))
    notes=div('measures',measure('A',L('10 s × 1 J = 10 J·s','10초 × 1 J = 10 J·s'),'blue')+measure('B',L('1 s × 10 J = 10 J·s','1초 × 10 J = 10 J·s'),'blue')+measure('C',L('1 s × 1 J = 1 J·s','1초 × 1 J = 1 J·s'),'gold'))
    return fig('efficiency-tradeoff',L('An explicit energy-time tradeoff','에너지와 시간을 함께 계산하기'),L('All three systems achieve the same verified performance.','세 시스템이 달성한 유효 성과는 같다.'),div('plot-pair',plot+notes),L('A and B tie. C scores ten times higher. These are hypothetical systems under the proposed rule.','A와 B는 동점이며 C의 점수는 열 배다. 제안한 규칙을 가상의 시스템에 적용했다.'))

def energy():
    def ops(items):
        return div('ops',''.join(div('op',f'<span>{i}.</span><div>{label}<strong>{v}</strong></div>') for i,(label,v) in enumerate(items,1)))
    hardware=ops([(L('Integer add / 32 bit','정수 덧셈 / 32비트'),'0.1 pJ'),(L('FP multiply / 32 bit','부동소수점 곱셈 / 32비트'),'4 pJ'),(L('64-bit cache read / 8 KB','64비트 캐시 읽기 / 8 KB'),'10 pJ'),(L('DRAM read / 64 bit','DRAM 읽기 / 64비트'),'1,300–2,600 pJ')])
    bio=ops([(L('Translation / amino acid','단백질 번역 / 아미노산'),'≈ 26×'+note(L('Own bound: kBT ln 20','자체 하한: kBT ln 20'))),(L('DNA copying / nucleotide','DNA 복사 / 뉴클레오타이드'),'≈ 165×'+note(L('Own bound: kBT ln 4','자체 하한: kBT ln 4')))])
    body=div('energy-section',div('panel-title',L('A. Hardware: energy per operation','A. 하드웨어: 연산당 에너지'))+note(L('Horowitz (2014), slide 32. Rough 45 nm estimates.','Horowitz (2014), 슬라이드 32. 대략적인 45 nm 추정치.'))+div('plot-pair',hardware+chart('hardware-energy',L('Rows 1 to 4 correspond to the four operations listed.','1~4번은 옆에 적은 네 연산에 해당한다.'),'',L('pJ per operation (log scale)','연산당 pJ (로그 척도)'))))
    body+=div('energy-section',div('panel-title',L('B. Biology: cost relative to its own bound','B. 생물학: 각 연산의 자체 하한 대비 비용'))+note(L('Kempes et al. (2017). Idealized uniform alphabets.','Kempes 외 (2017). 균일한 알파벳을 가정한 모형.'))+div('plot-pair',bio+chart('biology-energy',L('Rows 1 and 2 have ratios of approximately 26 and 165.','1번과 2번의 비율은 각각 약 26배와 165배다.'),'',L('Multiple of the bound (log scale)','하한의 배수 (로그 척도)'))))
    return fig('energy-ladder',L('Compare the same kind of cost','같은 종류의 비용끼리 비교하기'),L('The two panels use different denominators.','두 패널의 분모는 서로 다르다.'),body,L('A uses pJ per operation. B divides each energy estimate by that operation’s own bound. Neither panel ranks intelligence.','A는 연산당 pJ를 쓴다. B는 각 연산의 에너지를 해당 연산의 자체 하한으로 나눈다. 어느 패널도 지능 순위가 아니다.'))

def still():
    body=panel(L('Condition','성립 조건'),copy(L('The system does not alter its driving signal.','시스템이 자신을 구동하는 신호를 바꾸지 않는다.')))
    body+=div('result',L('Information retained about the current signal','현재 신호에 관해 기억한 정보'))
    body+=div('columns',panel(L('Predictive part','예측에 쓰이는 부분'),copy(L('Information about the next signal.','다음 신호에 관한 정보.')),'blue')+panel(L('Nonpredictive part','예측에 쓰이지 않는 부분'),copy(L('The difference between memory and predictive information.','기억 정보와 예측 정보의 차이.')),'gold'))
    body+=note(L('Schematic split. Box sizes are not measurements.','이해를 돕기 위한 구분이다. 상자 크기는 측정값이 아니다.'))
    body+=div('flow','↓')
    body+=panel(L('Dissipated work in the driving step','구동 단계에서 소산된 일'),div('formula','<span>= k<sub>B</sub>T ln 2</span><span>× (I<sub>mem</sub> − I<sub>pred</sub>)</span>'),'gold')
    body+=div('result',L('One bit of this difference: 2.87 × 10⁻²¹ J at 300 K.','이 차이의 1비트: 300 K에서 2.87 × 10⁻²¹ J.'))
    return fig('still-ledger',L('A physical link between memory and prediction','기억과 예측 사이의 물리적 연결'),L('Still et al. (2012), Eq. 14. Information expressed in bits.','Still 외 (2012), 식 14. 정보량은 비트로 표현했다.'),body,L('The equality applies to the stated driving step. The complete process can dissipate additional work.','등식은 명시한 구동 단계에 적용된다. 전체 과정에서는 추가로 일이 소산될 수 있다.'))

BUILDERS=[four_axes,scoreboard,input_test,output_futures,future_tree,horizon,blackwell,physical_ranges,multimodal_rate,efficiency,energy,still]

def build(korean_review=False):
    global LANG
    manifest=[]
    for LANG in (['en','ko'] if korean_review else ['en']):
        destination = KO_OUT if LANG == 'ko' else OUT
        destination.mkdir(parents=True, exist_ok=True)
        for make in BUILDERS:
            text=make()
            # Validate the emitted HTML subset as XML, including nested SVG.
            ET.fromstring(text)
            name=re.search(r'data-visual-id="([^"]+)"',text)[1]
            p=destination/f'fig-{name}{".ko" if LANG=="ko" else ""}.html'
            p.write_text(text)
            manifest.append({'id':name,'lang':LANG,'path':str(p.relative_to(ROOT))})
    report_dir = ROOT / '_workspace/physical-units-checks'
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir/'responsive-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(manifest)} responsive figure snippets.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--korean-review', action='store_true', help='Also generate the private Korean figure translations.')
    build(parser.parse_args().korean_review)
