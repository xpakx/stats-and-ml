use anyhow::Result;
use polars::prelude::*;

fn main() -> Result<()> {
    let teams = LazyCsvReader::new("data/teams.csv")
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

    let measures = teams
        .lazy()
        .sort(
            ["age"],
            sort_options
        )
        .select([col("age").cast(DataType::Float64)])
        .select([
            col("age").mean().alias("mean_age"),
            col("age").slice(0, 5).mean().alias("mean_5_youngest"),
            col("age").median().alias("median_age"),
        ])
        .collect()?;

    println!("{}", measures);

    Ok(())
}

