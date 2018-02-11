use std::str;
use std::process::Command;

fn main() {
    let err_msg = "command failed in rust";

    let from_cmd = Command::new("ls")
                         .output()
                         .expect(err_msg);

    // below it still works...

    if from_cmd.status.success() {

        let input = from_cmd.stdout;

        let n_lines = count_lines(&input);

        let strlist = convert_bytes2chars(&input);

        let files: Vec<&str> = strlist.split("\n").collect();

        println!("{} number of lines", n_lines);

        println!("first file is: {}", files[0]);

        println!("last file is: {:?}", files[files.len() - 1]);


    } else {
        println!("command failed");
    }

}


fn count_lines(vob: &[u8]) -> i64 {
    // vob: vector of bytes
    let mut line_count: i64 = 0;

    for &item in vob.iter() {
        if item == b'\n' {
            line_count += 1;
        }
    }

    if vob[vob.len() - 1] != b'\n' {
        line_count += 1;
    }

    line_count
}


fn convert_bytes2chars(vob: &[u8]) -> &str {
    // vob: vector of bytes
    let s = match str::from_utf8(vob) {
        Ok(v) => v,
        Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
    };

    s
}
