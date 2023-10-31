using UnityEngine;
using System.Linq;
using System.IO;
using com.heparo.terrain.toolkit;
using UnityEditor;
using static UnityEditor.Experimental.GraphView.GraphView;
using UnityEngine.UI;
using UnityEngine.Rendering;
//using UnityEngine.UIElements;

public class RawHeightmapLoader : MonoBehaviour
{
    public Terrain terrain;

    public GameObject gameObj;


    void Start()
    {
        Texture2D miniMapa2d = Resources.Load<Texture2D>("teste");

        Sprite mapaSprite = Sprite.Create(miniMapa2d, new Rect(0.0f, 0.0f, miniMapa2d.width, miniMapa2d.height), new Vector2(0.5f, 0.5f));

        gameObj.GetComponent<UnityEngine.UI.Image>().sprite = mapaSprite;

        if (terrain == null)
        {
            Debug.LogError("This script must be attached to a terrain object.");
            return;
        }
        int resolution = 1000;
        string rawFilePath = Application.dataPath + "/output_3d.raw";

        if (!File.Exists(rawFilePath))
        {
            Debug.LogError("The specified raw file path does not exist.");
            return;
        }

        byte[] rawBytes = File.ReadAllBytes(rawFilePath);
        float[,] heights = new float[resolution, resolution];

        for (int i = 0; i < resolution; i++)
        {
            for (int j = 0; j < resolution; j++)
            {
                float normalizedHeight = rawBytes[i * resolution + j] / 255f;
                heights[i, j] = normalizedHeight;
            }
        }

        terrain.terrainData.SetHeights(0, 0, heights);

        float[] slopeStops = new float[] { 60.0f, 75.0f };
        float[] heightStops = new float[] { 0.01648352f, 0.06593407f, 0.2527473f, 0.6483517f };

        Texture2D[] textures = Resources.LoadAll<Texture2D>("Textures");

        var toolKit = terrain.GetComponent<TerrainToolkit>();
        toolKit.TextureTerrain(slopeStops, heightStops, textures);
    }

    private Texture2D ScaleTexture(Texture2D source, int targetWidth, int targetHeight)
    {
        Texture2D result = new Texture2D(targetWidth, targetHeight, source.format, false);

        float incX = (1.0f / (float)targetWidth);
        float incY = (1.0f / (float)targetHeight);

        for (int i = 0; i < targetHeight; ++i)
        {
            for (int j = 0; j < targetWidth; ++j)
            {
                Color newColor = source.GetPixelBilinear((float)j / (float)targetWidth, (float)i / (float)targetHeight);
                result.SetPixel(j, i, newColor);
            }
        }

        result.Apply();
        return result;
    }
}
