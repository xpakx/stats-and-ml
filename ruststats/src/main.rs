use anyhow::Result;
use polars::prelude::*;

fn main() -> Result<()> {
    let mut teams = LazyCsvReader::new("data/teams.csv")
            .with_has_header(true)
            .finish()?
            .collect()?;
    println!("{}", teams.head(Some(10)));

    let sort_options = SortMultipleOptions { 
        descending: vec![false], 
        nulls_last: vec![false], 
        multithreaded: true, 
        maintain_order: false, 
        limit: None
    };
    teams.sort_in_place(["age"], sort_options)?;

    println!("After sorting:\n{}", teams.head(Some(10)));

    let ages = teams
        .lazy()
        .select([col("age").cast(DataType::Float64)])
        .collect()?;

    let mean_age = ages
        .clone()
        .lazy()
        .select([col("age").mean().alias("average_age")])
        .collect()?;

    println!("Mean age:\n{}", mean_age);

    let mean_age = ages
        .clone()
        .lazy()
        .slice(0, 5)
        .select([col("age").mean().alias("average_age")])
        .collect()?;

    println!("Mean age (5 youngest):\n{}", mean_age);

    let median_age = ages
        .clone()
        .lazy()
        .select([col("age").median().alias("median_age")])
        .collect()?;

    println!("Median age:\n{}", median_age);

    Ok(())
}

