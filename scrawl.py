import core
import model

def get_communitylist():
	res = []
	for community in model.Community.select():
		res.append(community.title)
	return res

if __name__=="__main__":
    regionlist = [u'chaoyang'] # only pinyin support
    model.database_init()
    #core.GetCommunityByRegionlist(regionlist) # Init,scrapy celllist and insert database; could run only 1st time
    communitylist = get_communitylist() # Read celllist from database
    core.GetHouseByCommunitylist(communitylist)
    core.GetRentByCommunitylist(communitylist)
    core.GetSellByCommunitylist(communitylist)
