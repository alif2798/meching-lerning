private VisualRecognition vrClient;
private CameraHelper helper;
 
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
 
   
    vrClient = new VisualRecognition(
            VisualRecognition.VERSION_DATE_2016_05_20,
            getString(R.string.api_key)
    );
 
    helper = new CameraHelper(this);
}

<Button
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_alignParentBottom="true"
    android:text="Take picture"
    android:onClick="takePicture"/>
 
<TextView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:id="@+id/detected_objects"
    android:layout_alignParentTop="true"/>
 
<ImageView
    android:layout_width="match_parent"
    android:layout_height="200dp"
    android:scaleType="fitCenter"
    android:id="@+id/preview"
    android:layout_below="@+id/detected_objects"/>

    public void takePicture(View view) {
}
@Override
protected void onActivityResult(int requestCode, 
                                int resultCode, 
                                Intent data) {
    super.onActivityResult(requestCode, resultCode, data);
     
    if(requestCode == CameraHelper.REQUEST_IMAGE_CAPTURE) {
    }
}
final Bitmap photo = helper.getBitmap(resultCode);
final File photoFile = helper.getFile(resultCode);
ImageView preview = findViewById(R.id.preview);
preview.setImageBitmap(photo);
AsyncTask.execute(new Runnable() {
    @Override
    public void run() {
        VisualClassification response =
                    vrClient.classify(
                            new ClassifyImagesOptions.Builder()
                                    .images(photoFile)
                                    .build()
                    ).execute();

    }
});
ImageClassification classification = 
                        response.getImages().get(0);
                         
VisualClassifier classifier = 
                        classification.getClassifiers().get(0);

final StringBuffer output = new StringBuffer();
for(VisualClassifier.VisualClass object: classifier.getClasses()) {
    if(object.getScore() > 0.7f)
        output.append("<")
              .append(object.getName())
              .append("> ");
}
 
runOnUiThread(new Runnable() {
    @Override
    public void run() {
        TextView detectedObjects = 
                findViewById(R.id.detected_objects);
        detectedObjects.setText(output);
    }
});
