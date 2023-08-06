SEQUANA
############


.. image:: https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)
   :target: http://bioconda.github.io/recipes/sequana/README.html

.. image:: https://badge.fury.io/py/sequana.svg
    :target: https://pypi.python.org/pypi/sequana

.. image:: https://github.com/sequana/sequana/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/sequana/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/github/sequana/sequana/badge.svg?branch=master
    :target: https://coveralls.io/github/sequana/sequana?branch=master

.. image:: http://readthedocs.org/projects/sequana/badge/?version=master
    :target: http://sequana.readthedocs.org/en/latest/?badge=master
    :alt: Documentation Status

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
   :target: http://joss.theoj.org/papers/10.21105/joss.00352
   :alt: JOSS (journal of open source software) DOI


:Python version: 3.7, 3.8, 3.9
:Documentation: `On readthedocs <http://sequana.readthedocs.org/>`_
:Issues: `On github <https://github.com/sequana/sequana/issues>`_
:How to cite: Citations are important for us to carry on developments.
    For Sequana library (including the pipelines), please use

    Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of
    Open Source Software, 2(16), 352, `JOSS DOI doi:10.21105/joss.00352 <https://joss.theoj.org/papers/10.21105/joss.00352>`_

    For the **genome coverage** tool (sequana_coverage):  Dimitri Desvillechabrol,
    Christiane Bouchier, Sean Kennedy, Thomas Cokelaer
    http://biorxiv.org/content/early/2016/12/08/092478

    For **Sequanix**: Dimitri Desvillechabrol, Rachel Legendre, Claire Rioualen,
    Christiane Bouchier, Jacques van Helden, Sean Kennedy, Thomas Cokelaer.
    Sequanix: A Dynamic Graphical Interface for Snakemake Workflows
    Bioinformatics, bty034, https://doi.org/10.1093/bioinformatics/bty034
    Also available on bioRxiv (DOI: https://doi.org/10.1101/162701)


**Sequana** includes a set of pipelines related to NGS (new generation sequencing) including quality control, variant calling, coverage, taxonomy, transcriptomics. We also ship **Sequanix**, a graphical user interface for Snakemake pipelines.

+------------------------------------------------+--------------------------+-----------------------+
| **pipeline or tools**                          | **Latest Pypi verison**  |  **Test passing**     |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/sequana_pipetools   |     |pipetools_pypi|     | |pipetools_test|      |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/sequana-wrappers    |        not on pypi       | |wrappers_test|       |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/demultiplex         |      |demultiplex_pypi|  |  |demultiplex_test|   |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/fastqc              |         |fastqc_pypi|    |  |fastqc_test|        |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/mapper              |         |mapper_pypi|    |  |mapper_test|        |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/pacbio_qc           |         |pacbio_qc_pypi| |  |pacbio_qc_test|     |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/ribofinder          |         |ribo_pypi|      |  |ribo_test|          |
+------------------------------------------------+--------------------------+-----------------------+
| https://github.com/sequana/rnaseq              |         |rnaseq_pypi|    |  |rnaseq_test|        |
+------------------------------------------------+--------------------------+-----------------------+



.. |pipetools_pypi| image:: https://badge.fury.io/py/sequana-pipetools.svg
    :target: https://pypi.python.org/pypi/sequana_pipetools

.. |pipetools_test| image:: https://github.com/sequana/sequana_pipetools/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/sequana_pipetools/actions/workflows/main.yml

.. |wrappers_test| image:: https://github.com/sequana/sequana-wrappers/actions/workflows/main.yml/badge.svg
    :target: https://github.com/sequana/sequana-wrappers/actions/workflows/main.yml

.. |fastqc_pypi| image:: https://badge.fury.io/py/sequana-fastqc.svg
    :target: https://pypi.python.org/pypi/sequana-fastqc

.. |fastqc_test| image:: https://github.com/sequana/fastqc/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/fastqc/actions/workflows/main.yml

.. |ribo_pypi| image:: https://badge.fury.io/py/sequana-ribofinder.svg
    :target: https://pypi.python.org/pypi/sequana-ribofinder

.. |ribo_test| image:: https://github.com/sequana/ribofinder/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/ribofinder/actions/workflows/main.yml

.. |mapper_pypi| image:: https://badge.fury.io/py/sequana-mapper.svg
    :target: https://pypi.python.org/pypi/sequana-mapper

.. |mapper_test| image:: https://github.com/sequana/mapper/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/mapper/actions/workflows/main.yml

.. |pacbio_qc_pypi| image:: https://badge.fury.io/py/sequana-pacbio-qc.svg
    :target: https://pypi.python.org/pypi/sequana-pacbio-qc

.. |pacbio_qc_test| image:: https://github.com/sequana/pacbio_qc/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/pacbio_qc/actions/workflows/main.yml


.. |demultiplex_pypi| image:: https://badge.fury.io/py/sequana-demultiplex.svg
    :target: https://pypi.python.org/pypi/sequana-demultiplex

.. |demultiplex_test| image:: https://github.com/sequana/demultiplex/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/demultiplex/actions/workflows/main.yml


.. |rnaseq_pypi| image:: https://badge.fury.io/py/sequana-rnaseq.svg
    :target: https://pypi.python.org/pypi/sequana-rnaseq

.. |rnaseq_test| image:: https://github.com/sequana/rnaseq/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/sequana/rnaseq/actions/workflows/main.yml

**Please see the** `documentation <http://sequana.readthedocs.org>`_ for an
up-to-date status and documentation.

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.12.7    * Fix memory leak in len() of FastA class
0.12.6    * remove some useless rules
0.12.5    * refactorisation of VCF tools/modules to use vcfpy instead of pyVCF
0.12.4    * complete change log before 0.12.4 on readthedocs.org
========= ====================================================================

