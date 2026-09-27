set1={'Anastasia'}
print(set1)

set1=set('Anastasia')
print(set1)

set1=set({'cat':'mio','dog':'wang'})
print(set1 )

set1=set('cicihaha')
print(set1)#會自動去除重複的元素：字串裡重複出現的 c、i、h、a 只會被保留一份。
#沒有順序性（Unordered）：每次印出來字母的排列順序可能會不一樣。
set1.add('shaucici')
print(set1)#如上，add shaucici，但每次印出來字母的排列順序可能會不一樣，
set1.remove('h')#如果沒有h，會報錯，remove 會報錯。
#set1.remove('h','a')不行運作，一次只能刪除一個元素，若要刪除多個元素，需使用迴圈或其他方法。
print(set1)#如上，remove ha，但每次印出來字母的排列順序可能會不一樣，
set1.discard('a')#如果沒有 a 也不會報錯，remove 會報錯。
print(set1)

set1.update('1231')#一樣會被拆解成單個元素，並加入 set1 中，若有重複的元素則不會加入。
print(set1)

set1.pop()#會隨機刪除一個元素，並回傳該元素，若 set1 為空集合則會報錯。
#pop不接受任何參數，因為 set1 是無序的，所以無法指定要刪除哪一個元素。
print(set1)



