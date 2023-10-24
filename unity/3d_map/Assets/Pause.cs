using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pause : MonoBehaviour
{

    public static bool GameIsPaused = false;

    public GameObject pauseMenuUI;
    public GameObject playerPoint;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            if (GameIsPaused)
            {
                Resume();
            }
            else
            {
                PauseGame();
            }
        }
    }
    public void Resume()
    {
        pauseMenuUI.SetActive(false);
        playerPoint.SetActive(false);
        Time.timeScale = 1f;
        GameIsPaused = false;

    }
    void PauseGame()
    {
        pauseMenuUI.SetActive(true);
        playerPoint.SetActive(true);
        Time.timeScale = 0f;
        GameIsPaused = true;

    }
}
