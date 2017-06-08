/**
 * Created by Guanghui on 2017/6/8.
 */

function compare_two_date(a, b) {
  // a: string in format:
  // 2017-05-28T02:24:27.353531Z
  // new Date('2017-05-28T02:24:27.353531Z')
  at = new Date(a["created"]);
  bt = new Date(b["created"]);

  return bt - at;
}

// TODO: hash file name in js as in python
function hash_file_name(fname){

}