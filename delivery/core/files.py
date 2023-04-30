def upload_file(action, data):
    client = Minio(
        os.getenv("MINIO_HOSTNAME") + ":9000",
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False,
    )

    bucket_name = "bucket1"
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    else:
        print(f"Bucket {bucket_name} already exists")
    json_data = json.dumps(data)
    date_time = datetime.now()
    file_path = f"{action}/openweather-" + str(date_time) + ".json"
    client.put_object(
        bucket_name,
        file_path,
        io.BytesIO(bytes(json_data, "UTF-8")),
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type="application/json",
    )

    return {"bucket_name": bucket_name, "file_path": file_path}
