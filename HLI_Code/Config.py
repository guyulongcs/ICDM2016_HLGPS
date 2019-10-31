class Config():
    
    #file folder
    folder_base = "/Users/guyulong"
    folderData = folder_base+"/Data/dataset/LBSN/201309_foursquare_dataset_umn/"
    folderDataOri = "umn_foursquare_datasets/"
    folderDataParsed = "parsedData/"
    folderExp = "Exp/"
    folderRatio = "Ratio/"
    folderPic = "Pic/"
    fileUser = "users.dat"
    fileVenue = "venues.dat"
    fileCheckin = "checkins.dat"
    fileRating = "ratings.dat"
    fileSocialGraph = "socialgraph.dat"

    fileUserSet = "userSet.dat"
    fileUserCity = "userCity.dat"
    fileFlagCheck = "check_"
    fileVenueCity = "venueCity.dat"

    fileFriendDistance = "friendDistance"
    fileRatio = "Ratio"
    #fileCheckinNorm = "checkinsNorm.dat"
    #fileUserNorm = "usersNorm.dat"
    fileNorm = "Norm"

    fileCheckinColNum = 6
    fileUserColNum = 3
    fileVenueColNum = 3
    fileRatingColNum = 3

    #filt
    fileFilt = "filt"
    filtCountry="America"
    dictCountry={}
    dictCountry["America"]={}
    dictCountry["America"]={"latMin": 28, "latMax": 50, "lonMin": -125, "lonMax": -65}

    fileCity = "city"
    fileFull = "full"

    #resource
    folderResourse = "resource"
    fileUS = "US.txt"
    fileUSCity = "USCity.txt"
    fileCityByPopulation = "cityByPopulation.txt"

    #res
    fileHomeLoc = "HomeLoc"
    fileTrue = "True_"
    fileKnowHome= "KnowHome_"
    fileHasCheckin = "HasCheckin_"
    fileNot = "Not_"

    #db
    host = "localhost"
    port = "3306"
    user = "root"
    pwd = "root"
    database = "umn_foursquare"

    #analyse
    fileAnalyseVenue = "analyseVenue"

    #method
    methodVote = "Vote_"
    methodClustering = "Cluseter_"
    methodAvg = "Avg_"
    methodInfluenceGlobal = "InfluenceGlobal_"
    methodTrust = "Trust_"

    #clustering
    clustering_Singlepass = "c_Singlepass"
    clustering_Kmeans = "c_Kmeans"
    clustering_Hierarchical = "c_Hierarchical"


    #clustering_Kmeans_k = 2
    #clustering_Kmeans_Round = 10





    flagExp = True
    flagRatio = True


    fileSplitStr="\t"

    maxUserCnt = -1

    #checkin
    flagCheckinLocUseVenueLoc = False

    #exp
    flag_exp_only_check_user = False

    #generate data
    flag_exp_generate_exp_data = False
    flag_exp_generate_ratio_data = False

    #ratio
    r_user_hasCheckin = 1
    r_user_hasHomeLocation = 0.8

    #method
    #avg
    flag_method_avg = False

    #maxVote
    flag_method_maxVote = False
    #flag: if not in city list, find nearest city
    flag_maxvote_nearCity = True

    #clustering
    flag_method_clustering = False
    flag_clustering_nearCity = True


    dictParamsClustering = {
        clustering_Kmeans: {"K":2, "Round": 10},
        clustering_Singlepass: {"threshold_dis_max": 10},
        clustering_Hierarchical: {"n_clusters":2, "threshold_cluster": 10, "flagFiltTimeInNight": True}
    }
    clusteringMethods = [clustering_Singlepass]
    clusteringMethods = dictParamsClustering.keys()

    #influenceGlobal
    flag_method_influenceGlobal = False

    threshold_coverage_disAvg = 10
    threshold_coverage_diffInfUser = 0.01

    #trust
    flag_method_trust = True
    #flag: broad method, decrease trust
    flag_method_trust_broadcast = False
    r_trust_iteration_alpha = 1
    #flag: use rating data
    flag_trust_use_rating = True
    #flag: trust coef between friends
    flag_method_trust_coef = True
    flag_method_trust_coef_jaccard = False
    flag_method_trust_coef_sigmoid = True
    #flag: user has checkin, cal direct, not update
    flag_method_trust_init_rating_user_loc = True
    flag_method_trust_not_update_loc_user_has_checkin = True
    flag_method_trust_update_loc_user_has_checkin_use_rating = False
    #flag: update user has checkin use friend loc
    flag_method_trust_update_loc_user_has_checkin_use_friend = False
    #flag: use real checkin loc, not venue loc
    flag_method_trust_use_checkin_loc_real = True
    trust_iterOutMax = 5
    trust_iterInnerMax = 10

    #weight
    weight_friend=1.
    weight_checkin=0.2
    weight_rating=0.2

    #result
    threshold_predict_err_mile = 100
    const_mile_km = 1.609344
    threshold_predict_err_km = threshold_predict_err_mile * const_mile_km

    flag_home_loc_identify = True

    file_exp_result_mile_accuracy = "mile_accuracy"
    file_exp_result_errdis = "errdis"
    file_exp_result_errcdf = "errcdf.pdf"

