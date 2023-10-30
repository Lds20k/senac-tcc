using UnityEngine;
using System.Linq;
using System.IO;
using com.heparo.terrain.toolkit;
using UnityEditor;
using static UnityEditor.Experimental.GraphView.GraphView;
using UnityEngine.UI;
//using UnityEngine.UIElements;

public class RawHeightmapLoader : MonoBehaviour
{
    public Terrain terrain;

    public Image imagem;


    void Start()
    {


        Texture2D miniMapa2d = Resources.Load<Texture2D>("teste");

        Sprite mapaSprite = Sprite.Create(miniMapa2d, new Rect(0.0f, 0.0f, 512,512), new Vector2(0.5f, 0.5f));

        imagem.sprite = mapaSprite;
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

        float[] slopeStops = new float[] { 60.0f, 75.0f };
        float[] heightStops = new float[] { 0.01648352f, 0.06593407f, 0.2527473f, 0.6483517f };

        Texture2D[] textures = Resources.LoadAll<Texture2D>("Textures");
        terrain.terrainData.SetHeights(0, 0, heights);

        var toolKit = terrain.GetComponent<TerrainToolkit>();
        toolKit.TextureTerrain(slopeStops, heightStops, textures);
    }
}
