provider "google" {
  credentials = file("gcp-service-key.json")
  project     = "rawg-data-pipeline"
  region      = "us-east1" # Change based on where you live
}

resource "google_bigquery_dataset" "video_game_dataset" {
  dataset_id                  = "video_game_dataset"
  project                     = "rawg-data-pipeline"
  friendly_name               = "Video Game Dataset"
  description                 = "Dataset for storing video game-related data"
  labels                      = { environment = "production" }

  access {
    role                        = "OWNER" # Adjust permissions as needed
    user_by_email               = "andrewkimka@gmail.com" # Change to your actual email
  }
}

resource "google_bigquery_table" "video_game_data" {
  dataset_id                  = google_bigquery_dataset.video_game_dataset.dataset_id
  table_id                    = "video_game_data"
  project                     = "rawg-data-pipeline"
  schema {
    fields {
      name                    = "name"
      type                    = "STRING"
    }
    fields {
      name                    = "release_date"
      type                    = "STRING"
    }
    fields {
      name                    = "genre"
      type                    = "STRING"
    }
    fields {
      name                    = "rating"
      type                    = "FLOAT"
    }
    fields {
      name                    = "game_id"
      type                    = "INT64"
    }
    fields {
      name                    = "playtime"
      type                    = "INTEGER"
    }
    fields {
      name                    = "year"
      type                    = "INTEGER"
    }
    fields {
      name                    = "month"
      type                    = "STRING"
    }
    fields {
      name                    = "week"
      type                    = "STRING"
    }
  }
}

resource "google_storage_bucket" "rawg-data-pipeline-bucket" {
  name                        = "rawg-data-pipeline-bucket"
  project                     = "rawg-data-pipeline"
  location                    = "us-east1"
}

resource "google_storage_bucket_object" "video_game_data_object" {
  name                        = "video_game_data.csv"
  bucket                      = google_storage_bucket.rawg-data-pipeline-bucket.name
  source                      = "gs://rawg-data-pipeline-bucket/video_game_data.csv"
  content_type                = "application/csv"
}

# Grant permissions to a service account to access the bucket
resource "google_storage_bucket_iam_member" "service_account_access" {
  bucket      = google_storage_bucket.rawg-data-pipeline-bucket.name
  role        = "roles/storage.objectViewer"
  member      = "serviceAccount:rawg-data-pipeline@rawg-data-pipeline.iam.gserviceaccount.com"
}
