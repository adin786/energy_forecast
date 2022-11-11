terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 2.13.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "lambda" {
  name = "lambda"
  build {
    path = "."
    tag  = ["lambda:latest"]
    dockerfile = "Dockerfile.lambda"
    label = {
      author : "Azam Din"
    }
  }
  triggers = {
    dir_sha1 = sha1(join("", [for f in fileset(path.module, "lambda_app/*") : filesha1(f)]))
  }
}

resource "docker_container" "lambda_container" {
  image = docker_image.lambda.latest
  name  = "lambda_container"
  ports {
    internal = 8080
    external = 8000
  }
}