mod central_tendency;

use std::env;
use anyhow::{Ok, Result};
use central_tendency::example1;

fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();
    let mut num: Option<i32> = None;

    for (i, arg) in args.iter().enumerate() {
        if arg.starts_with("--example") {
            if args.len() > i+1 {
                num = Some(args[i+1].parse()?);
            }
        }
    }

    match num {
        Some(1) => example1()?,
        _ => println!("No example found for the given number"),
    }

    Ok(())
}

