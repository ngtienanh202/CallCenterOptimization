from tqdm import tqdm
from src.utils import libSort



def predicted(file, listTimeAvailabel, days, xgb_reg):
    listResult = []
    for i in tqdm(range(len(file.columns[0]))):
        for j in range(len(listTimeAvailabel)):
            perCent = []
            preds = xgb_reg.predict_proba([[file[file.columns[0]][i],
                                            file[file.columns[1]][i],
                                            file[file.columns[2]][i],
                                            listTimeAvailabel[j],
                                            days]])
            preds = preds.tolist()
            perCent.append(preds[0][1])
        GoodTime = libSort.nlargest(3,zip(perCent, listTimeAvailabel))
        listResult.append(GoodTime)
    return listResult