function compare(x, y) {
    var z = 0;
    var s = x.length + y.length;;

    x.sort();
    y.sort();
    var a = x.shift();
    var b = y.shift();

    while(a !== undefined && b !== undefined) {
        if (a === b) {
            z++;
            a = x.shift();
            b = y.shift();
        } else if (a < b) {
            a = x.shift();
        } else if (a > b) {
            b = y.shift();
        }
    }
    return z/s * 200;
}

console.log(compare(['123', '中文', 'hello'], ['123', '中文', 'hello']))
console.log(compare(['123', '中文', 'hello'], ['123', '中文', 'hello'].sort()))
console.log(compare(['123', '中文', 'hello'], ['123', '中文', 'hello'].reverse()))
console.log(compare(['123', '中文', 'hello','中2文'], ['12', '中2文', '123','中文3']))
console.log(compare(['123', '中文', 'hello'], ['中文', 'world', '456']))
console.log(compare(['123', '中3文', 'hello'], ['中文', 'world', '汉字']))

console.log(compare(['I want you know that'], ['I want you know that 2']))


function strSimilarity2Number(s, t){
    var n = s.length, m = t.length, d=[];
    var i, j, s_i, t_j, cost;
    if (n == 0) return m;
    if (m == 0) return n;
    for (i = 0; i <= n; i++) {
        d[i]=[];
        d[i][0] = i;
    }
    for(j = 0; j <= m; j++) {
        d[0][j] = j;
    }
    for (i = 1; i <= n; i++) {
        s_i = s.charAt (i - 1);
        for (j = 1; j <= m; j++) {
            t_j = t.charAt (j - 1);
            if (s_i == t_j) {
                cost = 0;
            }else{
                cost = 1;
            }
            d[i][j] = Minimum (d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1] + cost);
        }
    }
    return d[n][m];
}
//两个字符串的相似程度，并返回相似度百分比
function strSimilarity2Percent(s, t){
    var l = s.length > t.length ? s.length : t.length;
    var d = strSimilarity2Number(s, t);
    return (1-d/l).toFixed(4);
}
function Minimum(a,b,c){
    return a<b?(a<c?a:c):(b<c?b:c);
}

console.log(strSimilarity2Percent('love34','like34'));






// 将上一次的查询和动态列表里面的组装一下
function combineNewQuery(lastQuery,list) {

    let randomIndex = roll(0,list.length);
    let randomWord = list[randomIndex];
    let newQuery = lastQuery + ' ' + randomWord;
    return newQuery;
}

function getSubQuery(queryWords) {
    var incQueries = []
    var incQuery = "";
    var randomArray = new Array();
    for (var k = 0; k < queryWords.length ; k++) {
        randomIndex = roll(0,queryWords.length-1);
        if ( randomArray.indexOf(randomIndex) < 0)
            randomArray.push(randomIndex);
    }
    randomArray.sort()
    for ( k = 0; k < randomArray.length-1 && k < 5; k++) {
        incQuery += queryWords[randomArray[k]]+' ';
    }
    incQuery += queryWords[randomArray[k]];
    if (incQueries)
        incQueries.push(trim(incQuery));

    console.log(incQuery);
}
function trim(s)  {
    return s.replace(/\n/g,'');
}
function roll(min,max){
    return Math.floor(Math.random()*(max+1))+min;
}

getSubQuery("hah lol  ddd")