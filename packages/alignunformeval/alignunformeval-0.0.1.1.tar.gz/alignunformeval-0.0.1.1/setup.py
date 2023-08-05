# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alignunformeval']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'alignunformeval',
    'version': '0.0.1.1',
    'description': 'This is a python tool to evaluate alignment and uniformity of sentence embedding',
    'long_description': '# AlignUnformEval\nThis is a python tool to evaluate alignment and uniformity of sentence embedding like [SimCSE paper](https://arxiv.org/pdf/2104.08821.pdf).   \n\n[SimCSE paper](https://arxiv.org/pdf/2104.08821.pdf) explains alignment and uniformity as below:\n>  Given a distribution of positive\npairs p_pos, alignment calculates expected distance between embeddings of the paired instances (assuming representations are already normalized): \n<img src="https://latex.codecogs.com/gif.latex?\\ell_{\\rm align}:=\\mathbb{E}_{(x, x^{+})\\sim p_{\\rm pos}}\\left[\\| f(x)-f(x^{+}) \\|^{2} \\right]" />\n\n\n> On the other hand, uniformity measures how well\nthe embeddings are uniformly distributed:\n<img src="https://latex.codecogs.com/gif.latex?\\ell_{\\rm uniformity}:=\\log \\mathbb{E}_{(x, y) \\overset{i.i.d.}{\\sim}  p_{\\rm data}} \\left[e ^{ -2\\| f(x)-f(x^{+}) \\|^{2}}\\right]" />\n> where p_data denotes the data distribution. \n\n## Install\nby pip\n```\npip install alignuniformeval\n``` \n\nby source\n```\npip install https://github.com/akiFQC/AlignUnformEval\n```\n\n\n## Usage\nYou can easily evaluate alignment and uniformity with this library.  \nThis is a minimal example that evaluate alignment and uniformity of STS Benchmark.\n```\nfrom alignunformeval import STSBEval\n\nevaluator = STSBEval(sentence_encoder)\n# sentence_encoder is a callable from List[str] to numpy.array. The output numpy.array must be [dimention_of_sentence_vector].\nresult = evaluator.eval_summary()\n# result =  {"alignment": value_of_aligenment, "uniformity": value_of_uniformity}\n```\n`STSBEval` get callable whose input is `list` of `str` and output is n dimentional `numpy.array`.\n\n## Dataset\n\n### [STS Benchmark](https://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark)\nThis dataset (especially, `sts-dev.csv`) was used in [SimCSE paper](https://arxiv.org/pdf/2104.08821.pdf). In the paper, the threshold of similarity score was st at 4.0;  pairs of sentences whose similarity score is higher than 4.0 are used for evaluation of alignment. You can set other threshold as the following example.\n```\nfrom alignunformeval import STSBEval\n# sentence_encoder : some function List[str] to np.array[dimention_of_sentence_vector]\nevaluator = STSBEval(sentence_encoder, threshold=3.0) # set threshold at 3.0\nresult = evaluator.eval_summary()\n```\nPlease see `test/test_stsb.py` if you want more details.\n\n### [Tokyo Metropolitan University Paraphrase Corpus (TMUP)](https://github.com/tmu-nlp/paraphrase-corpus)\n[Tokyo Metropolitan University Paraphrase Corpus (TMUP)](https://github.com/tmu-nlp/paraphrase-corpus) is a Japanese paraphrase dataset.\n\n```\nfrom alignunformeval import TMUPEval\n# sentence_encoder : some function List[str] to np.array[dimention_of_sentence_vector]\nevaluator = TMUPEval(sentence_encoder)\nresult = evaluator.eval_summary()\n```\n\n## License \nThe license of this tool follows each dataset. Please read the documents of datasets you use.\n\n## Reference\n1. https://arxiv.org/pdf/2104.08821.pdf \n2. https://ixa2.si.ehu.eus/stswiki/index.php/STSbenchmark \n3. https://github.com/tmu-nlp/paraphrase-corpus\n\n',
    'author': 'akiFQC',
    'author_email': 'yakaredori@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/akiFQC/AlignUnformEval',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
