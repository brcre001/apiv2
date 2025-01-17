from breathecode.utils import Cache
from .models import Asset, AssetComment, AssetTechnology


class AssetCache(Cache):
    model = Asset
    depends = ['User', 'AssetTechnology', 'AssetCategory', 'KeywordCluster', 'AssetKeyword', 'Assessment']
    parents = ['AssetAlias', 'AssetErrorLog']


class AssetCommentCache(Cache):
    model = AssetComment
    depends = ['Asset', 'User']
    parents = []


class TechnologyCache(Cache):
    model = AssetTechnology
    depends = []
    parents = []
