import re
import logging
from urllib.parse import urljoin

import requests
from lxml import etree
import sympy
from sympy.parsing.latex import parse_latex

INTE_PATTERN = re.compile(r"(\\int_.*?\^.*?}\s)(.*?)(\{d\s*x\})")
PROBLEMS_PATTERN = re.compile(r"(\d+)\s*题")
LATEX_XPATH = etree.XPath('body/div/div/div/center/p')
PROBLEMS_XPATH = etree.XPath('body/div/div/div/div[@class="row"]/div/h1')
logger = logging.getLogger(__name__)

def logconfig(level=logging.INFO):
    '''设置DEBUG日志输出'''
    fmter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(fmter)
    logger.setLevel(level)
    logger.addHandler(handler)

class HTTPApi:
    url = "http://202.38.93.111:10190/"

    def __init__(self, token: str, cookies=None):
        self.token = token
        if cookies:
            self.session = requests.Session()
            self.session.cookies.update(cookies)
        else:
            self.session = None

    def get_firsttime(self):
        self.session = requests.Session()
        url = urljoin(self.url, "login")
        params = {"token": self.token}
        r = self.session.get(url, params=params)
        r.raise_for_status()
        return r

    def get(self):
        if self.session is None:
            return self.get_firsttime()
        r = self.session.get(self.url)
        logger.debug(f"{r.request.headers=}")
        r.raise_for_status()
        return r

    def submit(self, ans: float):
        url = urljoin(self.url, "submit")
        data = {"ans": ans}
        r = self.session.post(url, data=data)
        logger.debug(f"{r.request.headers=}")
        r.raise_for_status()
        return r


def get_latex(html: str) -> str:
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    elements = LATEX_XPATH(tree)
    return elements[0].text.strip(" $")

def parse_integrate(latex: str):
    match = INTE_PATTERN.match(latex)
    if not match:
        logger.error(f"LaTeX match error! {latex=}")
        raise ValueError("LaTeX match error!", latex)
    int_, expr, dx = match.groups()
    logger.debug(f"{int_=}, {expr=}, {dx=}")
    return match.groups()

def preprocess_latex(latex: str) -> str:
    latex = latex.replace("\\,", "")\
                 .replace("\\left", "")\
                 .replace("\\right", "")\
                 .strip()
    int_, expr, dx = parse_integrate(latex)
    latex = int_ + "(" + expr + ")" + dx
    return latex

def eval_latex(latex: str) -> float:
    latex = preprocess_latex(latex)
    expr = parse_latex(latex)
    ans = expr.evalf()
    logger.info(f"{ans=}, {expr=}")
    return ans

def solve_a_problem(api: HTTPApi):
    r = api.get()
    latex = get_latex(r.text)
    ans = eval_latex(latex)
    return r, api.submit(ans)

def get_problem_num(r: requests.Response) -> int:
    parser = etree.HTMLParser()
    tree = etree.fromstring(r.text, parser)
    text = PROBLEMS_XPATH(tree)[0].text.strip()
    num = int(PROBLEMS_PATTERN.match(text).group(1))
    return num

def main(token):
    if token is None:
        token = input("Token: ")
    cookies = {}
    api = HTTPApi(token, cookies)
    try:
        i = 400
        while i:
            logger.info(f"还剩下{i}题...")
            rget, rsubmit = solve_a_problem(api)
            i = get_problem_num(rget)
    finally:
        print(f"rget.text={rget.text}\n"
              f"rsubmit.text={rsubmit.text}\n"
              f"{api.session.cookies=}")


if __name__ == "__main__":
    token = None
    logconfig()
    main(token)
