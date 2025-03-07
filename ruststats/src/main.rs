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
        ..Default::default()
    };

    let measures = teams
        .clone()
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


    let sort_options = SortMultipleOptions { 
        descending: vec![true], 
        ..Default::default()
    };

    let age_counts = teams
        .clone()
        .lazy()
        .select([col("age").cast(DataType::Float64)])
        .group_by([col("age")])
        .agg([
            col("age").count().alias("count")
        ])
        .sort(
            ["count"],
            sort_options
        )
        .collect()?;

    println!("{}", age_counts.clone().head(Some(10)));
    let max = age_counts
        .lazy()
        .select([col("count").max()])
        .collect()?;
    println!("{}", max);

    Ok(())
}

