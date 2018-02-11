use std::process::Command;

fn main() {

    let err_msg = "command failed in rust";

    Command::new("ls")
        .arg("-l")
        .arg("-a")
        .spawn()
        .expect(err_msg);

}


