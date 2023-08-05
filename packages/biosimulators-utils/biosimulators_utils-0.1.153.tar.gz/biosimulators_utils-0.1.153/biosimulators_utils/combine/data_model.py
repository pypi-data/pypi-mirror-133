""" Data model for COMBINE/OMEX archives

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2020-12-06
:Copyright: 2020, Center for Reproducible Biomedical Modeling
:License: MIT
"""

from ..utils.core import are_lists_equal, none_sorted
from ..data_model import Person  # noqa: F401
import abc
import datetime  # noqa: F401
import enum

__all__ = [
    'CombineArchiveBase',
    'CombineArchive',
    'CombineArchiveContent',
    'CombineArchiveContentFormat',
    'CombineArchiveContentFormatPattern',
]


class CombineArchiveBase(abc.ABC):
    """ A COMBINE/OMEX archive """
    pass


class CombineArchive(CombineArchiveBase):
    """ A COMBINE/OMEX archive

    Attributes:
        contents (:obj:`list` of :obj:`CombineArchiveContent`): contents of the archive
    """

    def __init__(self, contents=None):
        """
        Args:
            contents (:obj:`list` of :obj:`CombineArchiveContent`, optional): contents of the archive
        """
        self.contents = contents or []

    def get_master_content(self):
        """ Get the master content of an archive

        Returns:
            :obj:`list` of :obj:`CombineArchiveContent`: master content
        """
        master_content = []
        for content in self.contents:
            if content.master:
                master_content.append(content)
        return master_content

    def to_tuple(self):
        """ Tuple representation of a COMBINE/OMEX archive

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation of a COMBINE/OMEX archive
        """
        contents = tuple(none_sorted(content.to_tuple() for content in self.contents))
        return (contents)

    def is_equal(self, other):
        """ Determine if two content items are equal

        Args:
            other (:obj:`CombineArchiveContent`): another content item

        Returns:
            :obj:`bool`: :obj:`True`, if two archives are equal
        """
        return self.__class__ == other.__class__ \
            and are_lists_equal(self.contents, other.contents)


class CombineArchiveContent(CombineArchiveBase):
    """ A content item (e.g., file) in a COMBINE/OMEX archive

    Attributes:
        location (:obj:`str`): path to the content
        format (:obj:`str`): URL for the specification of the format of the content
        master (:obj:`bool`): :obj:`True`, if the content is the "primary" content of the parent archive
    """

    def __init__(self, location=None, format=None, master=False):
        """
        Args:
            location (:obj:`str`, optional): path to the content
            format (:obj:`str`, optional): URL for the specification of the format of the content
            master (:obj:`bool`, optional): :obj:`True`, if the content is the "primary" content of the parent archive
        """
        self.location = location
        self.format = format
        self.master = master

    def to_tuple(self):
        """ Tuple representation of a content item of a COMBINE/OMEX archive

        Returns:
            :obj:`tuple` of :obj:`str`: tuple representation of a content item of a COMBINE/OMEX archive
        """
        return (self.location, self.format, self.master)

    def is_equal(self, other):
        """ Determine if two content items are equal

        Args:
            other (:obj:`CombineArchiveContent`): another content item

        Returns:
            :obj:`bool`: :obj:`True`, if two content items are equal
        """
        return self.__class__ == other.__class__ \
            and self.location == other.location \
            and self.format == other.format \
            and self.master == other.master


class CombineArchiveContentFormat(str, enum.Enum):
    """ Format for the content of COMBINE/OMEX archives """
    AI = 'http://purl.org/NET/mediatypes/application/pdf'
    BMP = 'http://purl.org/NET/mediatypes/image/bmp'
    BNGL = 'http://purl.org/NET/mediatypes/text/bngl+plain'
    BioPAX = 'http://identifiers.org/combine.specifications/biopax'
    C = 'http://purl.org/NET/mediatypes/text/x-c'
    CellML = 'http://identifiers.org/combine.specifications/cellml'
    CopasiML = 'http://purl.org/NET/mediatypes/application/x-copasi'
    CPP_HEADER = 'http://purl.org/NET/mediatypes/text/x-c++hdr'
    CPP_SOURCE = 'http://purl.org/NET/mediatypes/text/x-c++src'
    DLL = 'http://purl.org/NET/mediatypes/application/vnd.microsoft.portable-executable'
    DOC = 'http://purl.org/NET/mediatypes/application/msword'
    DOCX = 'http://purl.org/NET/mediatypes/application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    CSV = 'http://purl.org/NET/mediatypes/text/csv'
    EPS = 'http://purl.org/NET/mediatypes/application/postscript'
    Escher = 'http://purl.org/NET/mediatypes/application/escher+json'
    GIF = 'http://purl.org/NET/mediatypes/image/gif'
    GINML = 'http://purl.org/NET/mediatypes/application/ginml+xml'
    GMSH_MESH = 'http://purl.org/NET/mediatypes/model/mesh'
    HDF5 = 'http://purl.org/NET/mediatypes/application/x-hdf'
    HOC = 'http://purl.org/NET/mediatypes/text/x-hoc'
    HTML = 'http://purl.org/NET/mediatypes/text/html'
    INI = 'http://purl.org/NET/mediatypes/text/x-ini'
    IPython_Notebook = 'http://purl.org/NET/mediatypes/application/x-ipynb+json'
    JavaScript = 'http://purl.org/NET/mediatypes/text/javascript'
    JPEG = 'http://purl.org/NET/mediatypes/image/jpeg'
    JSON = 'http://purl.org/NET/mediatypes/application/json'
    Kappa = 'http://purl.org/NET/mediatypes/text/x-kappa'
    LEMS = 'http://purl.org/NET/mediatypes/application/lems+xml'
    MASS = 'http://purl.org/NET/mediatypes/application/mass+json'
    MATLAB = 'http://purl.org/NET/mediatypes/text/x-matlab'
    MATLAB_DATA = 'http://purl.org/NET/mediatypes/application/x-matlab-data'
    MorpheusML = 'http://purl.org/NET/mediatypes/application/morpheusml+xml'
    NeuroML = 'http://identifiers.org/combine.specifications/neuroml'
    NuML = 'http://purl.org/NET/mediatypes/application/numl+xml'
    OMEX = 'http://identifiers.org/combine.specifications/omex'
    OMEX_MANIFEST = 'http://identifiers.org/combine.specifications/omex-manifest'
    OMEX_METADATA = 'http://identifiers.org/combine.specifications/omex-metadata'
    OWL = 'http://purl.org/NET/mediatypes/application/rdf+xml'
    PDF = 'http://purl.org/NET/mediatypes/application/PDF'
    pharmML = 'http://purl.org/NET/mediatypes/application/pharmml+xml'
    PNG = 'http://purl.org/NET/mediatypes/image/png'
    PPT = 'http://purl.org/NET/mediatypes/application/vnd.ms-powerpoint'
    PPTX = 'http://purl.org/NET/mediatypes/application/vnd.openxmlformats-officedocument.presentationml.presentation'
    Python = 'http://purl.org/NET/mediatypes/application/x-python-code'
    R = 'http://purl.org/NET/mediatypes/text/x-r'
    R_Project = 'http://purl.org/NET/mediatypes/application/x-r-project'
    RBA = 'http://purl.org/NET/mediatypes/application/rba+zip'
    RDF_XML = 'http://purl.org/NET/mediatypes/application/rdf+xml'
    RST = 'http://purl.org/NET/mediatypes/text/x-rst'
    RUBY = 'http://purl.org/NET/mediatypes/text/x-ruby'
    SBGN = 'http://identifiers.org/combine.specifications/sbgn'
    SBML = 'http://identifiers.org/combine.specifications/sbml'
    SBOL = 'http://identifiers.org/combine.specifications/sbol'
    SBOL_VISUAL = 'http://identifiers.org/combine.specifications/sbol-visual'
    Scilab = 'http://purl.org/NET/mediatypes/application/x-scilab'
    SED_ML = 'http://identifiers.org/combine.specifications/sed-ml'
    SimBiology_Project = 'http://purl.org/NET/mediatypes/application/x-sbproj'
    Smoldyn = 'http://purl.org/NET/mediatypes/text/smoldyn+plain'
    SO = 'http://purl.org/NET/mediatypes/application/x-sharedlib'
    SVG = 'http://purl.org/NET/mediatypes/image/svg+xml'
    SVGZ = 'http://purl.org/NET/mediatypes/image/svg+xml'
    TEXT = 'http://purl.org/NET/mediatypes/text/plain'
    TIFF = 'http://purl.org/NET/mediatypes/image/tiff'
    TSV = 'http://purl.org/NET/mediatypes/text/tab-separated-values'
    VCML = 'http://purl.org/NET/mediatypes/application/vcml+xml'
    Vega = 'http://purl.org/NET/mediatypes/application/vnd.vega.v5+json'
    Vega_Lite = 'http://purl.org/NET/mediatypes/application/vnd.vegalite.v3+json'
    WEBP = 'http://purl.org/NET/mediatypes/image/webp'
    XML = 'http://purl.org/NET/mediatypes/application/xml'
    XPP = 'http://purl.org/NET/mediatypes/text/x-xpp'
    XLS = 'http://purl.org/NET/mediatypes/application/vnd.ms-excel'
    XLSX = 'http://purl.org/NET/mediatypes/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    XUL = 'http://purl.org/NET/mediatypes/text/xul'
    XYZ = 'http://purl.org/NET/mediatypes/chemical/x-xyz'
    YAML = 'http://purl.org/NET/mediatypes/application/x-yaml'
    ZGINML = 'http://purl.org/NET/mediatypes/application/zginml+zip'
    ZIP = 'http://purl.org/NET/mediatypes/application/zip'
    OTHER = 'http://purl.org/NET/mediatypes/application/octet-stream'


class CombineArchiveContentFormatPattern(str, enum.Enum):
    """ Format for the content of COMBINE/OMEX archives """
    AI = r'^https?://purl\.org/NET/mediatypes/(application/pdf|application/postscript)$'
    BMP = r'^https?://purl\.org/NET/mediatypes/image/bmp$'
    BNGL = r'^https?://purl\.org/NET/mediatypes/text/bngl\+plain($|\.)'
    BioPAX = r'^https?://identifiers\.org/combine\.specifications/biopax($|\.)'
    C = r'^https?://purl\.org/NET/mediatypes/text/x-c$'
    CellML = r'^https?://identifiers\.org/combine\.specifications/cellml($|\.)'
    CPP_HEADER = r'^https?://purl\.org/NET/mediatypes/text/x-c\+\+hdr$'
    CPP_SOURCE = r'^https?://purl\.org/NET/mediatypes/text/x-c\+\+src$'
    CopasiML = r'^https?://purl\.org/NET/mediatypes/application/x-copasi$'
    CSV = r'^https?://purl\.org/NET/mediatypes/text/csv$'
    DLL = r'^https?://purl\.org/NET/mediatypes/application/vnd\.microsoft\.portable-executable$'
    DOC = r'^https?://purl\.org/NET/mediatypes/application/msword$'
    DOCX = r'^https?://purl\.org/NET/mediatypes/application/vnd\.openxmlformats-officedocument\.wordprocessingml\.document$'
    EPS = r'^https?://purl\.org/NET/mediatypes/(application/postscript|application/eps|application/x-eps|image/eps|image/x-eps)$'
    Escher = r'^https?://purl\.org/NET/mediatypes/application/escher\+json$'
    GIF = r'^https?://purl\.org/NET/mediatypes/image/gif$'
    GINML = r'^https?://purl\.org/NET/mediatypes/application/ginml\+xml$'
    GMSH_MESH = r'^https?://purl\.org/NET/mediatypes/model/mesh$'
    HDF5 = r'^https?://purl\.org/NET/mediatypes/application/x-hdf5?$'
    HOC = r'^https?://purl\.org/NET/mediatypes/text/x-hoc$'
    HTML = r'^https?://purl\.org/NET/mediatypes/(text/html|application/xhtml\+xml)$'
    INI = r'^https?://purl\.org/NET/mediatypes/text/x-ini$'
    IPython_Notebook = r'^https?://purl\.org/NET/mediatypes/application/x-ipynb\+json$'
    JavaScript = r'^https?://purl\.org/NET/mediatypes/(text/javascript|text/x-javascript|application/javascript|application/x-javascript)$'
    JPEG = r'^https?://purl\.org/NET/mediatypes/image/jpeg$'
    JSON = r'^https?://purl\.org/NET/mediatypes/application/json$'
    Kappa = r'^https?://purl\.org/NET/mediatypes/text/x-kappa$'
    LEMS = r'^https?://purl\.org/NET/mediatypes/application/lems\+xml$'
    MASS = r'^https?://purl\.org/NET/mediatypes/application/mass\+json$'
    MATLAB = r'^https?://purl\.org/NET/mediatypes/text/x-matlab$'
    MATLAB_DATA = r'^https?://purl\.org/NET/mediatypes/application/x-matlab-data$'
    MorpheusML = r'^https?://purl\.org/NET/mediatypes/application/morpheusml\+xml$'
    NeuroML = r'^https?://identifiers\.org/combine\.specifications/neuroml($|\.)'
    NuML = r'^https?://purl\.org/NET/mediatypes/application/numl\+xml$'
    OMEX = r'^https?://identifiers\.org/combine\.specifications/omex($|\.)'
    OMEX_MANIFEST = r'^https?://identifiers\.org/combine\.specifications/omex-manifest($|\.)'
    OMEX_METADATA = r'^https?://identifiers\.org/combine\.specifications/omex-metadata($|\.)'
    OWL = r'^https?://purl\.org/NET/mediatypes/application/rdf\+xml$'
    PDF = r'^https?://purl\.org/NET/mediatypes/application/pdf$'
    pharmML = r'^https?://purl\.org/NET/mediatypes/application/pharmml\+xml$'
    PNG = r'^https?://purl\.org/NET/mediatypes/image/png$'
    PPT = r'^https?://purl\.org/NET/mediatypes/application/vnd\.ms-powerpoint$'
    PPTX = r'^https?://purl\.org/NET/mediatypes/application/vnd\.openxmlformats-officedocument\.presentationml\.presentation$'
    Python = r'^https?://purl\.org/NET/mediatypes/application/x-python-code$'
    R = r'^https?://purl\.org/NET/mediatypes/text/x-r$'
    R_Project = r'^https?://purl\.org/NET/mediatypes/application/x-r-project$'
    RBA = r'^https?://purl\.org/NET/mediatypes/application/rba\+zip$'
    RDF_XML = r'^https?://purl\.org/NET/mediatypes/application/rdf\+xml$'
    RST = r'^https?://purl\.org/NET/mediatypes/text/x-rst$'
    RUBY = r'^https?://purl\.org/NET/mediatypes/text/x-ruby$'
    SBGN = r'^https?://identifiers\.org/combine\.specifications/sbgn($|\.)'
    SBML = r'^https?://identifiers\.org/combine\.specifications/sbml($|\.)'
    SBOL = r'^https?://identifiers\.org/combine\.specifications/sbol($|\.)'
    SBOL_VISUAL = r'^https?://identifiers\.org/combine\.specifications/sbol-visual($|\.)'
    Scilab = r'^https?://purl\.org/NET/mediatypes/application/x-scilab$'
    SED_ML = r'^https?://identifiers\.org/combine\.specifications/sed\-?ml($|\.)'
    SimBiology_Project = r'^https?://purl\.org/NET/mediatypes/application/x-sbproj$'
    Smoldyn = r'^https?://purl\.org/NET/mediatypes/text/smoldyn\+plain$'
    SO = r'^https?://purl\.org/NET/mediatypes/application/x-sharedlib$'
    SVG = r'^https?://purl\.org/NET/mediatypes/image/svg\+xml$'
    SVGZ = r'^https?://purl\.org/NET/mediatypes/image/svg\+xml$'
    TEXT = r'^https?://purl\.org/NET/mediatypes/text/plain$'
    TIFF = r'^https?://purl\.org/NET/mediatypes/image/tiff$'
    TSV = r'^https?://purl\.org/NET/mediatypes/text/tab-separated-values$'
    Vega = r'^https?://purl\.org/NET/mediatypes/application/vnd\.vega\.v5\+json$'
    Vega_Lite = r'^https?://purl\.org/NET/mediatypes/application/vnd\.vegalite\.v3\+json$'
    VCML = r'^https?://purl\.org/NET/mediatypes/application/vcml\+xml$'
    WEBP = r'^https?://purl\.org/NET/mediatypes/image/webp$'
    XLS = r'^https?://purl\.org/NET/mediatypes/application/vnd\.ms-excel$'
    XLSX = r'^https?://purl\.org/NET/mediatypes/application/vnd\.openxmlformats-officedocument\.spreadsheetml\.sheet$'
    XML = r'^https?://purl\.org/NET/mediatypes/application/xml$'
    XPP = r'^https?://purl\.org/NET/mediatypes/text/x-xpp$'
    XUL = r'^https?://purl\.org/NET/mediatypes/text/xul$'
    XYZ = r'^https?://purl\.org/NET/mediatypes/chemical/x-xyz$'
    YAML = r'^https?://purl\.org/NET/mediatypes/application/x-yaml$'
    ZGINML = r'^https?://purl\.org/NET/mediatypes/application/zginml\+zip$'
    ZIP = r'^https?://purl\.org/NET/mediatypes/application/zip$'
    OTHER = r'^https?://purl\.org/NET/mediatypes/application/octet-stream$'
